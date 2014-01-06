import json
import logging
from minecraft_query import MinecraftQuery

class reportGenerator():
    def __init__(self, sfilename):
        sfile = open(sfilename)
        self.serverlist = json.load(sfile)
        sfile.close()

    def _query(self, hosts):
        logging.debug("Beginning query cycle")
        for server in hosts:
            logging.info("Querying %s", str(server))
            try:
                query = MinecraftQuery(hosts[server]["ip"], hosts[server]["port"])
                hosts[server]["status"]=query.get_status()
                logging.debug(json.dumps(hosts[server]["status"]))
            except:
                hosts[server]["status"]="OFFLINE"
                logging.warning("{0} appears to be offline!".format(str(server)))
        return hosts

    def update(self):
        logging.debug("Starting update cycle")
        report = self._query(self.serverlist)
        out = open("report.json", 'w')
        logging.info("Writting report")
        json.dump(report, out, indent=2)
        out.close()

class webFormater():
    def __init__(self, reportfile):
        rfile = open(reportfile)
        self.reportdata = json.load(rfile)
        rfile.close()
        self.page = open("index.html", 'w')

    def writeHeader(self):
        self.page.write("<html><head><title>Minecraft Server Status</title></head>")

    def writeBody(self):
        self.page.write("<table cellpadding=4px>")
        self.page.write("<th>Server Report</th>")
        for server in self.reportdata:
            self.page.write("<tr class=\"serverinfo\">")
            self.page.write("<td>{0}</td>".format(str(server)))
            if self.reportdata[server]["status"] != "OFFLINE": 
                self.page.write("<td>{0}".format(str(self.reportdata[server]["status"]["motd"])))
                self.page.write(" @ {0}".format(self.reportdata[server]["port"]))
                self.page.write("<td>{0}/{1}</td>".format(str(self.reportdata[server]["status"]["numplayers"]), str(self.reportdata[server]["status"]["maxplayers"])))
                self.page.write("</tr>")
            else:
                self.page.write("<td colspan=2>SERVER IS OFFLINE</td>")
        self.page.write("</table>")

    def writeFooter(self):
        self.page.write("</body>")
        self.page.write("</html>")

    def update(self):
        self.writeHeader()
        self.writeBody()
        self.writeFooter()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    reporter = reportGenerator("servers.json")
    reporter.update()
    writer = webFormater("report.json")
    writer.update()
