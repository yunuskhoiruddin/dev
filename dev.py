
import re, os, time

class Dev:
    def __init__(self):
        self.clear()
        self.dir = {
            'blueprint': 'blueprints/',
            'component': 'components/',
            'preview': 'src/demo/',
            'src': 'src/'
        }
        self.label = {
            'blueprint': '# Blueprint [default:index.html] : ',
            'start': '# Start Development [Press Ctrl+C to Stop]',
            'update': "- [{0}] Update : {1}",
            'stop': ' - Stop Development'
        }
        self.update = 0
        self.loop = {
            'current': 0,
            'limit': 10,
            'col': 0
        }
        self.sleep = 2
        self.blueprint = input(self.label['blueprint']) or 'index.html'
        print(self.label['start'])
        self.autoCreate()
    
    def create(self):
        html = self.readBlueprint()
        html = self.setComponent( html )
        self.writeFile( 'preview', self.blueprint, html )
        self.textUpdate()
        self.createFileSRC()

    def setloop(self):
        self.loop['current'] = self.loop['current'] + 1
        if self.loop['col'] >= self.loop['limit']:
            self.textreset()
            self.loop['col'] = 0
        else:
            self.loop['col'] = self.loop['col'] + 1 
        return str(self.loop['current'])

    def textUpdate(self):
        loop = self.setloop();
        t = time.localtime()
        t = time.strftime("%H:%M:%S",t)
        print( self.label['update'].format(t, loop) )

    def textreset(self):
        self.clear()
        print(self.label['blueprint']+self.blueprint)
        print(self.label['start'])

    def readBlueprint(self):
        file = open( self.dir['blueprint']+self.blueprint, 'r' )
        text = file.read()
        file.close()
        return text
    
    def setComponent(self, text):
        return re.sub( '([\t ]+)\[\# ([a-z]+) \]', self.replaceComponent, text )

    def replaceComponent(self, match):
        tab = match.group(1)
        key = match.group(2)
        return self.readComponent('body', tab, key, True)

    def readComponent(self, tag, tab, key, valempty):
        file = open( self.dir['component']+key+'.html', 'r' )
        text = file.read()
        file.close()
        text = self.tagComponent( text, tag, key, valempty ).strip("\n").replace("\n","\n"+tab)
        return ( "\n"+tab+text ).replace("\n    ","\n").lstrip("\n")

    def tagComponent(self, text, tag, key, valempty):
        valempty = ["    <!-- {0} ? -->".format(key)] if valempty else ['']
        return ( re.findall( r"<{0}>(.*)</{0}>".format(tag), text, flags= re.I | re.DOTALL ) or valempty )[0]

    def createFileSRC(self):
        listFiles = self.getallfile(True)
        styles = ''
        scripts = ''
        for file in listFiles:
            styles = self.readsrc( styles, 'style', file)
            scripts = self.readsrc( scripts, 'script', file)
        self.writeFile( 'src', 'style.css', styles )
        self.writeFile( 'src', 'script.js', scripts )

    def readsrc(self, source, tag, filename):
        text = self.readComponent (tag, '', filename, False )
        if text != '':
            return source + "\n\n/* {0} */\n\n".format(filename.upper()) + text
        return source;

    def writeFile(self, dir, file, content):
        file = open(self.dir[dir]+file, 'w+')
        file.write(content.strip("\n"))
        file.close()

    def autoCreate(self):
        try:
            bp = self.dir['blueprint']+self.blueprint
            listFiles = self.getallfile(False)
            listFiles.append(bp)
            update    = max([os.stat(file).st_mtime for file in listFiles ])
            if( self.update < update ):
                self.update = update
                self.create()
            time.sleep(self.sleep)
            self.autoCreate()
        except KeyboardInterrupt:
            print(self.label['stop']);

    def getallfile(self, listonly):
        listFiles = os.listdir(self.dir['component']);
        if listonly:
            return list( map( self.removeHTML, listFiles ) )
        else:
            return list( map( self.addPath, listFiles ) )
    
    def addPath(self, file):
        return self.dir['component']+file

    def removeHTML(self, file):
        return file.rstrip('.html')

    def clear(self):
        os.system( 'cls' if os.name == 'nt' else 'clear' )

if __name__ == '__main__':
    Dev()