#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import nltk
import codecs
import re
import string
import multiprocessing

class MainWindow(gtk.Window):
    def __init__(self):
        #Creazione Finestra
        gtk.Window.__init__(self)
        self.connect("delete_event", self.doQuit)
        self.set_size_request(400,400)
        self.set_title("Text Analyzer")
        color = gtk.gdk.color_parse('#efefef')
        self.modify_bg(gtk.STATE_NORMAL, color)
        self.set_border_width(5)

        #Creazione MenuBar=====================================================
        self.menubar = gtk.MenuBar()
        self.menu = gtk.Menu()
        self.menu2 = gtk.Menu()
        self.file = gtk.MenuItem('File')
        self.about = gtk.MenuItem('About')
        self.apri = gtk.MenuItem('Open')
        self.save = gtk.MenuItem('Save Output')
        self.chiudi = gtk.MenuItem('Quit')
        self.info = gtk.MenuItem('Info')
        self.menubar.append(self.file)
        self.menubar.append(self.about)
        self.menu.append(self.apri)
        self.menu.append(self.save)
        self.menu.append(self.chiudi)
        self.menu2.append(self.info)
        self.apri.connect_object("activate", self.openfile, "Open")
        self.save.connect_object("activate", self.savefile, "Save Output")
        self.chiudi.connect_object("activate", self.doQuit, "Quit")
        self.info.connect_object("activate", self.about_me,'About')
        self.file.set_submenu(self.menu)
        self.about.set_submenu(self.menu2)
        
        #Creazione Aree di testo
        self.buffer = gtk.TextBuffer()
        self.text = gtk.TextView(self.buffer)
        self.text.set_wrap_mode(gtk.WRAP_CHAR)
        self.text.set_right_margin(10)
        self.text.set_left_margin(10)
        self.text.set_editable(gtk.FALSE)
        self.buffer_2 = gtk.TextBuffer()
        self.text_2 = gtk.TextView(self.buffer_2)
        self.text_2.set_right_margin(10)
        self.text_2.set_left_margin(10)
        self.text_2.set_wrap_mode(gtk.WRAP_CHAR)
        self.text_2.set_editable(gtk.FALSE)

        #Creazione Toolbar
        self.toolbar = gtk.Toolbar()
        self.toolbar.set_style(gtk.TOOLBAR_BOTH)
        self.toolButTokenize = gtk.ToolButton(gtk.STOCK_DND)
        self.toolButTokenize.set_label('Sentences Splitter')
        self.toolButTokenize.connect("clicked", self.sentence_splitter)
        self.toolButWordTokenize = gtk.ToolButton(gtk.STOCK_DND)
        self.toolButWordTokenize.set_label('Word Tokenizer')
        self.toolButWordTokenize.connect("clicked", self.tokenizer)
        self.toolButBigrams = gtk.ToolButton(gtk.STOCK_DND)
        self.toolButBigrams.set_label('Bigrams')
        self.toolButBigrams.connect("clicked", self.bigrams)
        self.toolButTrigrams = gtk.ToolButton(gtk.STOCK_DND)
        self.toolButTrigrams.set_label('Trigrams')
        self.toolButTrigrams.connect("clicked", self.trigrams)
        self.toolButtOpen = gtk.ToolButton(gtk.STOCK_OPEN)
        self.toolButtOpen.set_label('Open Text')
        self.toolButtOpen.connect("clicked", self.openfile)
        self.separatore = gtk.SeparatorToolItem()
        self.toolbar.insert(self.toolButtOpen, 0)
        self.toolbar.insert(self.separatore, 1)
        self.toolbar.insert(self.toolButTokenize, 2)
        self.toolbar.insert(self.toolButWordTokenize, 3)
        self.toolbar.insert(self.toolButBigrams, 4)
        self.toolbar.insert(self.toolButTrigrams, 5)

        #Finestra regular Expression
        self.toolbar2 = gtk.Toolbar()
        self.entry = gtk.Entry()
        item = gtk.ToolItem()
        item.add(self.entry)
        item2 = gtk.ToolItem()
        label = gtk.Label(' <-- Enter a Pattern ')
        item_checkbox = gtk.ToolItem()
        self.checkbox = gtk.CheckButton('Real Time')
        item_checkbox.add(self.checkbox)
        self.checkbox.connect_object("toggled", self.real_time, 'Match!')
        item2.add(label)
        item3 = gtk.ToolItem()
        button_regexp = gtk.Button(' Match! ')
        button_regexp.connect_object("clicked", self.reg_exp_pattern,'Match!')
        item3.add(button_regexp)
        label1 = gtk.Label(' or replace --> ')
        item4 = gtk.ToolItem()
        item4.add(label1)
        item5 = gtk.ToolItem()
        item6 = gtk.ToolItem()
        item7 = gtk.ToolItem()
        item8 = gtk.ToolItem()
        self.entry2 = gtk.Entry()
        item5.add(self.entry2)
        label2 = gtk.Label(' in --> ')
        item6.add(label2)
        self.entry3 = gtk.Entry()
        item7.add(self.entry3)
        button2 = gtk.Button(' Replace! ')
        button2.connect_object("clicked", self.reg_exp_replace, 'Replace!')
        item8.add(button2)
        item9 = gtk.ToolItem()
        button3 = gtk.Button(' Save ')
        button3.connect_object("clicked", self.reg_exp_replace_saved, 'Save!')
        item9.add(button3)
        self.toolbar2.insert(item, 0)
        self.toolbar2.insert(item2, 1)
        self.toolbar2.insert(item3, 2)
        self.toolbar2.insert(item_checkbox,3)
        self.toolbar2.insert(item4, 4)
        self.toolbar2.insert(item5, 5)
        self.toolbar2.insert(item6, 6)
        self.toolbar2.insert(item7, 7)
        self.toolbar2.insert(item8, 8)
        self.toolbar2.insert(item9, 9)
  
        #Packing dei widget
        vbox = gtk.VBox(gtk.FALSE, 5)
        hbox = gtk.HBox(gtk.FALSE, 5)
        vbox.pack_start(self.menubar,gtk.FALSE,gtk.FALSE,0)
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw2 = gtk.ScrolledWindow()
        sw2.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(self.text)
        sw2.add(self.text_2)
        hbox.pack_start(sw)
        hbox.pack_start(sw2)
        self.notebook = gtk.Notebook()
        self.show_tabs = True
        self.show_border = True
        vbox.pack_start(self.notebook,gtk.FALSE,gtk.TRUE,0)
        self.notebook.show()
        self.notebook.append_page(self.toolbar,gtk.Label('Tokenizer'))
        self.notebook.append_page(self.toolbar2,gtk.Label('Regular Espression'))
        vbox.pack_start(self.toolbar, gtk.FALSE, gtk.FALSE, 0)
        vbox.pack_start(hbox, gtk.TRUE, gtk.TRUE, 0)
        self.add(vbox)
        self.statusbar = gtk.Statusbar()
        vbox.pack_start(self.statusbar,gtk.FALSE, gtk.FALSE, 0)
        self.show_all()

         #Funzioni
    
    def doQuit(self, widget, data=None):
        gtk.main_quit()

    def openfile(self, widget, data = None):
        self.apri = gtk.FileChooserDialog(title = 'Open File', parent = None, action = gtk.FILE_CHOOSER_ACTION_OPEN, \
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK), backend = None)
        self.response = self.apri.run()
        if self.response == gtk.RESPONSE_OK:
            self.file = self.apri.get_filename()
            self.file2 = codecs.open(self.file, 'r','utf-8')
            self.raw = self.file2.read()
            self.raw_2 = string.lower(self.raw)
            self.buffer.set_text(self.raw_2)
            self.apri.destroy()
            file_input = self.raw_2
            frasi = nltk.word_tokenize(file_input)
            self.length = len(frasi)
            vocabolario = set(frasi)
            self.statusbar.push(0, "Corpus : " + str(self.length) + ' tokens\t\tVocabulary : ' + str(len(vocabolario)) + ' types')
            

        elif self.response == gtk.RESPONSE_CANCEL:
            self.apri.destroy()
    
    def savefile(self, widget, data=None):
        self.salva = gtk.FileChooserDialog(title = 'Save Output', parent = None, action = gtk.FILE_CHOOSER_ACTION_SAVE,\
        buttons = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK), backend = None)
        self.response2 = self.salva.run()
        if self.response2 == gtk.RESPONSE_OK:
            filename = self.salva.get_filename()
            text = self.buffer_2.get_text(self.buffer_2.get_start_iter(), self.buffer_2.get_end_iter())
            output = str(text)
            foo = open(filename, "w")
            foo.write(output)
            self.salva.destroy()
        elif self.response2 == gtk.RESPONSE_CANCEL :
            self.salva.destroy()

    def sentence_splitter(self, widget, data = None):
      file_input = self.raw_2
      sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
      frasi = sent_tokenizer.tokenize(file_input)
      frase = ''
      for i in frasi:
          frase += "\n\n" + i
      self.buffer_2.set_text(frase)
    
    def estrai_token(self, frasi):
        tokensTOT = []
        for frase in frasi:
            tokens = nltk.word_tokenize(frase) #tokenizzo il testo
            tokensTOT = tokensTOT + tokens
        return tokensTOT #restituisce un array con tutti i tokens del testo
    
    def tokenizer(self, widget, data = None):
        file_input = self.raw_2
        frasi = nltk.word_tokenize(file_input)
        tokensTOT = ''
        for i in frasi:
          tokensTOT += "\n" + i + '\t\n  -  Frequency: '+ str(frasi.count(i)) +'\t Frequency average : ' + str(frasi.count(i) * 1.0 / self.length * 1.0) + "\n"
        self.buffer_2.set_text(tokensTOT)
        
    def frequenza_bigramma(self, bigrammi_diversi, bigrammi):
        freq_bigramma_max = 0.0
        for bigramma in bigrammi_diversi:
            frequenza_bigramma = bigrammi.count(bigramma)
            if frequenza_bigramma > freq_bigramma_max:
                freq_bigramma_max = frequenza_bigramma
                bigramma_MAX = bigramma
        return bigramma_MAX, freq_bigramma_max
            
    def bigrams(self, widget, data = None):
        file_input = self.raw_2
        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        frasi = sent_tokenizer.tokenize(file_input)
        testo_tokenizzato = self.estrai_token(frasi)
        bigrammi = nltk.bigrams(testo_tokenizzato)
        bigrammi_diversi = set(bigrammi)
        bigramma_MAX2, freq_bigramma_max2 = self.frequenza_bigramma(bigrammi_diversi, bigrammi)
        bigramsTOT = "Most frequent bigram : " + str(bigramma_MAX2) + "\tFrequency : " + str(freq_bigramma_max2) + '\n\n'
        for i in bigrammi:
            bigramsTOT += "\n" + str(i) +'\t\n  -  Frequency: '+ str(bigrammi.count(i)) +'\tFrequency average : ' + str(bigrammi.count(i) * 1.0 / self.length * 1.0) + "\n"
        self.buffer_2.set_text(bigramsTOT)
    
    def frequenza_trigramma(self, trigrammi_diversi, trigrammi):
        freq_trigramma_max = 0.0
        for trigramma in trigrammi_diversi:
            frequenza_trigramma = trigrammi.count(trigramma)
            if frequenza_trigramma > freq_trigramma_max:
                freq_trigramma_max = frequenza_trigramma
                trigramma_MAX = trigramma
        return trigramma_MAX, freq_trigramma_max
        
    def trigrams(self, widget, data = None):
        file_input = self.raw_2
        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        frasi = sent_tokenizer.tokenize(file_input)
        testo_tokenizzato = self.estrai_token(frasi)
        trigrammi = nltk.trigrams(testo_tokenizzato)
        trigrammi_diversi = set(trigrammi)
        trigramma_MAX2, freq_trigramma_max2 = self.frequenza_trigramma(trigrammi_diversi, trigrammi)
        trigramsTOT = "Most frequent trigram : " + str(trigramma_MAX2) + "\Frequency : " + str(freq_trigramma_max2) + '\n\n'
        for i in trigrammi:
            trigramsTOT += "\n" + str(i) +'\t\n  -  Frequency: '+ str(trigrammi.count(i)) +'\t Frequency average : ' + str(trigrammi.count(i) * 1.0 / self.length * 1.0) + "\n"
        self.buffer_2.set_text(trigramsTOT)
        
    def reg_exp_pattern(self, widget, data = None):
        corpus = self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter())
        pattern = self.entry.get_text()
        try:
            new_text = re.findall(pattern,corpus)
            new_text2 = 'n)\tMatch\n\n'
            c = 0
            for i in new_text:
                 c+=1
                 new_text2 += str(c) +  '\t' + i + '\n'
            self.buffer_2.set_text(str(new_text2))
        except:
            self.buffer_2.set_text('Wrong Regex')


    def real_time(self, widget, data = None):
        if self.checkbox.get_active() == True:
            self.entry_id = self.entry.connect("changed", self.reg_exp_pattern)
        elif self.checkbox.get_active() == False:
            self.entry.disconnect(self.entry_id)

    def reg_exp_replace(self, widget, data = None):
        file_input = self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter())
        pattern = self.entry2.get_text()
        replace = self.entry3.get_text()
        try:
            self.new_text = re.sub(pattern, replace, file_input)
            self.buffer_2.set_text(str(self.new_text))
        except:
            self.buffer_2.set_text('Wrong Regex')

        
    def reg_exp_replace_saved(self, widget, data = None):
         self.buffer.set_text(self.buffer_2.get_text(self.buffer_2.get_start_iter(), self.buffer_2.get_end_iter()))
    
    def about_me(self, widget, data = None):
        about = gtk.Window()
        about.set_size_request(200,200)
        label = gtk.Label('Text Analyzer \n\n\n\tBy\n\n\tGiancarlo Buomprisco')
        about.add(label)
        about.show_all()
    
    def main(self):
        gtk.main()
     
if __name__ == "__main__":
    go = MainWindow()
    proc = multiprocessing.Process(target=go.main())
    proc.start()
    proc.join()
    
    

