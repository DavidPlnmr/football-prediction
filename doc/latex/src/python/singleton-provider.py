__instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Provider, cls).__new__(cls)    
            load_dotenv()
            log_path = './log/app.log'
            logging.basicConfig(filename=log_path, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
            cls.__api_facade = ApiFacade(os.getenv("API_KEY"), log_path)
            cls.__db_manager = DbManager("127.0.0.1", os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), log_path)
        return cls.__instance