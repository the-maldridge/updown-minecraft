import json
import logging
from minecraft_query import MinecraftQuery

def init():
    logging.basicConfig(level = logging.INFO)
    sfile = open("servers.json")
    serverlist = json.load(sfile)
    sfile.close()
    return serverlist

def query(hosts):
    logging.debug("Beginning query cycle")
    for server in hosts:
        logging.info("Querying %s", str(server))
        query = MinecraftQuery(hosts[server]["ip"], hosts[server]["port"])
        hosts[server]["status"]=query.get_status()
        logging.debug(json.dumps(hosts[server]["status"]))
    return hosts

def main(servers):
    logging.debug("Starting update cycle")
    report = query(servers)
    out = open("report.json", 'w')
    logging.info("Writting report")
    json.dump(report, out, indent=2)
    out.close()

if __name__ == "__main__":
    servers = init()
    main(servers)
