import json
import logging
from minecraft_query import MinecraftQuery

def init():
    logging.basicConfig(defaultLevel = logging.INFO)

def main():
    logging.debug("Beginning query")
    query = MinecraftQuery("10.0.0.36", 25565)
    basic_status = query.get_status()
    print "The server has %d players" % (basic_status['numplayers'])
    print basic_status


if __name__ == "__main__":
    init()
    main()
