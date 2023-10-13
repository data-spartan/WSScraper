import threading
import sys
import websocket
from redis_db import redis_hash
from utils.parser_tools import *
from utils.retrier import *
from typing import AnyStr,List,Dict,Any,Callable
import orjson
from dataclasses import dataclass,field
from time import sleep
# from constants import random_ids_list,scrapoxy_admin_pass_base64
from logger.log_func import *

@dataclass
class WebsocketClient:
    ws_url: AnyStr = field(default=str,repr=False)
    miss_keys_redis: List = field(default_factory=list, repr=False)
    markets_redis: List[Dict]= field(default_factory=dict, repr=False)
    result_redis: List[Dict]= field(default_factory=dict, repr=False)
    random_ids_list: List= field(default_factory=lambda: pd.read_csv(getenv("ids_random_path"),header=None)[0].to_list(),repr=False)
    parsers: Any = field(default_factory=Parsers,repr=False)
    
    def __post_init__(self):
        self.fh, self.logg = logging_func("ws", getenv("main_logs"))
        self.pill2kill = threading.Event() #---ensures if error happens that potential hanging thread is closed
        self.conn_closed_count=0
        self.error_count=0
    

    def subsription(self,ws: websocket.WebSocketApp) -> None:
        self.logg.info(f"{threading.current_thread().name} thread started. Thread id: {threading.get_ident()}")
        while not self.pill2kill.is_set():
            """
            first request is for matches data, second for related markets;
            need to add sleep(2) bcs sometimes happens that there are no messages to read from, so socket closes connection and error fires up.
            """

            ws.send(
                '{"command":"get","params":{"source":"betting","what":{"sport":["id","name","alias","order"],"competition":["id","order","name"],"region":["id","name","alias"],"game":[["id","start_ts","team1_name","team2_name","type","info","stats","markets_count","is_blocked","video_provider"]]},"where":{"game":{"type":1},"sport":{"id":{"@in":[1]}}},"subscribe":false},"rid":"2"}')
            ws.send(
                '{"command": "get", "params": {"source": "betting", "is_betslip": true, "what": {"sport":["id"],"game": ["id", "is_blocked", "team1_name", "team2_name", "team1_reg_name", "team2_reg_name", "is_live"], "market": ["base", "type", "name", "home_score", "away_score", "cashout", "extra_info"], "event": ["id", "price", "type", "type_1", "name", "base", "ew_allowed"]},"where":{"sport":{"id":{"@in":[1]}},"game":{"is_live":1}}}, "subscribe": false}, "rid": "2"}')
            sleep(15)

    def on_open(self, ws:websocket.WebSocketApp):
        self.logg.info(f"Websocket({ws}) connection opened.")
        self.pill2kill.clear()
        ws.send(
            f'{{"command":"request_session","params":{{"language":"eng","site_id":1,"release_date":"26/05/2022-12:10"}},"rid":{2}}}')
        """
        starting separate thread for asynchronous websocketAPP, bcs main thread is occupied with maintaining websocketAPP,
        making thread daemonic prevents thread hanging in case of encountering various errors and warnings.
        """
        sub_thread = threading.Thread(target=self.subsription, args=[ws], name="subscription", daemon=True)
        sub_thread.start()

    def on_msg(self, ws: websocket.WebSocketApp,msg: bytes) -> None:
        message_decoded = orjson.loads(msg)
        """
        using orjson instead of json lib gives huge perf boosts of cca 520 %
        """
        if message_decoded["data"] and not "sid" in message_decoded["data"]:
            raw_data = message_decoded["data"]["data"]["sport"]

            """
            detecting markets/macthes info; if "name" in msg then it is match info, otherwise it is markets info;
            """
            if "name" in raw_data[next(iter(raw_data))]:
                old_result = self.result_redis.load_results_data()
                result_info = self.parsers.match_info_parser(raw_data,old_result)
                fill_missing = self.parsers.fill_missing_data_keys(result_info,self.random_ids_list,self.miss_keys_redis)
                self.result_redis.save_results(fill_missing)
            else:
                old_markets=self.markets_redis.load_markets_data()
                markets_info=self.parsers.markets_parser(raw_data,old_markets)
                self.markets_redis.save_markets(markets_info)

    
    def on_error(self, ws: websocket.WebSocketApp, error:websocket.WebSocketException):
        self.pill2kill.set()
        if error.__str__() == "Connection to remote host was lost.":
            if self.conn_closed_count < 3:
                self.conn_closed_count+=1
            else:
                self.logg.warning(f"{error}. Number od disconnections {self.conn_closed_count}")
                self.conn_closed_count = 0
                self.pill2kill.clear()
                ws.close()
        else:
            self.error_count += 1
            if self.error_count < 3:
                self.logg.error(f"{error}. Number of errors {self.error_count}")
                #sleep(3)
            else:
                
                self.logg.error(f"{error}. Number of errors {self.error_count}", exc_info=True)
                self.error_count=0
                self.pill2kill.clear()
                ws.close()
    
    def on_close(self,ws, close_status_code, close_msg):
        if self.pill2kill.is_set():
            self.logg.warning(f"CLOSED CONNECTION!")
            sleep(1)
            self.connection()
        else:
            return

    # @auto_recovery
    def connection(self) -> None:
        websocket.enableTrace(traceable=False, handler=None)
        websocket.setdefaulttimeout(15)
        ws = websocket.WebSocketApp(self.ws_url,
                                    on_open=self.on_open,
                                    on_message=self.on_msg,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        """
        adding skip_utf8_validation=True for performance boost of cca 5%.
        """
        ####add webscoket conn through proxy when project is pushed on prod server
        ws.run_forever(skip_utf8_validation=True)


