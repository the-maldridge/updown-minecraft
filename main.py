import json
import logging
from minecraft_query import MinecraftQuery

def init():
    logging.basicConfig(defaultLevel = logging.INFO)
    sfile = open("servers.json")
    serverlist = json.load(sfile)
    sfile.close()
    return serverlist

def query(hosts):
    logging.debug("Beginning query cycle")
    for host in hosts:
        logging.info("Querying %s", str(host))
        query = MinecraftQuery(hosts[host]["ip"], hosts[host]["port"])
        hosts[host]["status"]=query.get_status()
    return hosts

def main(servers):
    logging.debug("Beginning query")
    report = query(servers)
    print report
    out = open("report.json", 'w')
    json.dump(report, out, indent=2)
    out.close()

if __name__ == "__main__":
    servers = init()
    main(servers)
