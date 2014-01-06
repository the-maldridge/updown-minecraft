import json
import logging
from minecraft_query import MinecraftQuery

class reportGenerator():
    def __init__(self, sfilename):
        logging.basicConfig(level = logging.INFO)
        sfile = open(sfilename)
        self.serverlist = json.load(sfile)
        sfile.close()

    def _query(self, hosts):
        logging.debug("Beginning query cycle")
        for server in hosts:
            logging.info("Querying %s", str(server))
            query = MinecraftQuery(hosts[server]["ip"], hosts[server]["port"])
            hosts[server]["status"]=query.get_status()
            logging.debug(json.dumps(hosts[server]["status"]))
        return hosts

    def update(self):
        logging.debug("Starting update cycle")
        report = self._query(self.serverlist)
        out = open("report.json", 'w')
        logging.info("Writting report")
        json.dump(report, out, indent=2)
        out.close()

if __name__ == "__main__":
    reporter = reportGenerator("servers.json")
    reporter.update()
