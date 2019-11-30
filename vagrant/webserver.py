# Web werver for ubuntu 16.04 using python3
# * for server featrues
from http.server import BaseHTTPRequestHandler, HTTPServer
# * for POST -> input output
import cgi

# * for database manipulations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(engine)
session = DBSession()


class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):

                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset = utf-8')
                self.end_headers()

                restaurants = session.query(Restaurant).all()
                output = ""
                output += "<html><body><h2>"

                for item in restaurants:
                    output += item.name + "<br>"
                    output += "<a href = '/restaurants/"+str(item.id)+"/edit'>Edit</a><br>"
                    output += "<a href = '/restaurants/"+str(item.id)+"/remove'>Remove</a><br><br>"

                output += "<a href = '/restaurants/new'>Make a New Restaurant Here</a>"
                output += "</h2></body></html>"

                self.wfile.write(output.encode("utf-8"))
                return
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset = utf-8')
                self.end_headers()
                urlParsed = self.path.split("/")
                idToEdit = int(urlParsed[urlParsed.index("edit")-1])

                toEdit = session.query(Restaurant).filter_by(id = idToEdit).one()

                output = ""
                output += "<html><body>"
                output += "<h1>"
                output += toEdit.name
                output += "</h1>"

                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/"+str(idToEdit)+"/edit'>"
                output += '<input name = "newRestaurantName" type = "text">'
                output += '<input type = "submit" value = "Rename">'
                output += "</form>"



                output += "</body></html>"
                
                
                self.wfile.write(output.encode("utf-8"))
                return
            if self.path.endswith("/remove"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset = utf-8')
                self.end_headers()
                urlParsed = self.path.split("/")
                idToEdit = int(urlParsed[urlParsed.index("remove")-1])

                toEdit = session.query(Restaurant).filter_by(id = idToEdit).one()

                output = ""
                output += "<html><body>"
                output += "<h2>"
                output += "Are you sure you want to remove " + toEdit.name + "?"
                output += "</h2>"

                output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/"+str(toEdit.id)+"/remove'>"
                output += "<input type = 'submit' value = 'Remove'>"
                output += "</form>"
                
                output += "<a href = 'restaurants'>Cancel</a>"
                output += "</body></html>"
                
                self.wfile.write(output.encode("utf-8"))
                return
            if self.path.endswith("/confirmed"):
                self.send_response(301)

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset = utf-8')
                self.end_headers()

                output = ""
                output += "<html><body>"

                output += "<h1>"
                output += "Make a New Restaurant<br>"
                output += "</h1>"

                output += '''<form method='POST' enctype='multipart/form-data'
                 action='/restaurants/new'>
                 <input name="newRestaurantName" type="text" ><input type="submit" value="Create"> </form>'''

                output += "</body></html>"

                self.wfile.write(output.encode("utf-8"))
                return
            

        except:
            self.send_error(404, "File not found: " +
                            self.path, self.path.encode("utf-8"))
            print("erro")

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = pdict['boundary'].encode("utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                
                messagecontent = fields.get("newRestaurantName")

            
                newRestaurant = Restaurant(name=messagecontent[0].decode("utf-8"))
                session.add(newRestaurant)
                session.commit()
                self.send_response(301)

                self.send_header('Location','/restaurants')
                self.end_headers()
            
                return
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                pdict['boundary'] = pdict['boundary'].encode("utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                
                messagecontent = fields.get("newRestaurantName")

                urlParsed = self.path.split("/")
                idToEdit = urlParsed[urlParsed.index("edit")-1]

                toEdit = session.query(Restaurant).filter_by(id = idToEdit).one()
                
                toEdit.name = messagecontent[0].decode("utf-8")
                session.add(toEdit)
                session.commit()

                self.send_response(301)

                self.send_header('Location','/restaurants')
                self.end_headers()
            
                return

            if self.path.endswith("/remove"):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                urlParsed = self.path.split("/")
                idToEdit = urlParsed[urlParsed.index("remove")-1]

                toEdit = session.query(Restaurant).filter_by(id = idToEdit).one()
                session.delete(toEdit)
                session.commit()

                self.send_response(301)
                self.send_header('Location','/restaurants')
                self.end_headers()
            
                return
        except Exception as e:
            print("error occured: ", e)


def htmlmessage(msg, headertype="h1"):
    if headertype not in ["h1", "h2", "h3"]:
        print("sth wrong")
        headertype = "h3"

    return "<html><body><{h1}>{msg1}</{h1}><body><html>".format(h1=headertype, msg1=msg)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebserverHandler)
        print("Web server running on port ", port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
