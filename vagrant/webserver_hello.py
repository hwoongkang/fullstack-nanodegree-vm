from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                
                self.send_response(200)
                self.send_header('Content-type','text/html; charset = utf-8')
                self.end_headers()

                output = b"<html><body>Hello!</body></html>"
                
                try:
                    self.wfile.write(output)
                except:
                    print("wfile wrong",output)
                
                return
            if self.path.endswith("/hola"):
                
                self.send_response(200)
                self.send_header('Content-type','text/html; charset = utf-8')
                self.end_headers()

                output = "<html><body>&#161Hola!  <a href = '/hello'>Back to Hello</a></body></html>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                try:
                    self.wfile.write(output.encode("utf-8"))
                except:
                    print("wfile wrong",output)
                
                return
            else:
                self.send_error(404, "File not found: ", self.path)
                
        except:
            self.send_error(404,"File not found: " + self.path, self.path.encode("utf-8"))
            print("erro")
    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()
            
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = pdict['boundary'].encode("utf-8")
            if ctype == 'multipart/form-data':
                
                fields = cgi.parse_multipart(self.rfile, pdict)
                
                messagecontent = fields.get("message")
            
            output = ""
            output += "<html><body>"
            
            output += " <h2> Okay, how about this: </h2>"
            
            output += "<h1> %s </h1>" % messagecontent[0].decode("utf-8")
            
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output.encode("utf-8"))
            print(output)
        except Exception as e:
            print("error occured: ",e)
def main():
    try:
        port = 8080
        server = HTTPServer(('',port),WebserverHandler)
        print("Web server running on port ",port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()