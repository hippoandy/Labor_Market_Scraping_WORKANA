import threading
import queue
import os

from googletrans import Translator

# translate group of text with multithreading
class Translate():
    # constructor
    def __init__( self, name='trans', concurrent=30 ):
        self.name = name
        self.concurrent = concurrent
        self.text_list = []
        self.job_queue = queue.Queue()
        self.translator = Translator()
    # set the data to be parsed
    def input( self, text_list ):
        if( not self.text_list ): self.text_list = text_list
        return self
    # ignitiate the thread
    def run( self ):
        self._spawn()
        for text in self.text_list: self.job_queue.put( text )
        self.job_queue.join()
    # things for the thread to do
    def _job( self ):
        obj = self.job_queue.get()
        obj[ 'translated' ] = self.translator.translate( obj[ 'original' ] , dest='en' ).text
        self.job_queue.task_done()
    # creating the threads
    def _spawn( self ):
        for _ in range( 0, self.concurrent ):
            t = threading.Thread( target=self._job )
            t.daemon = True
            t.start()