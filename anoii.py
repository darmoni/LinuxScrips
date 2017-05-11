# -*- coding: utf-8 -*-
word ="תזיז אחד מ".decode('UTF-8')
rtl_move_message =''.join(reversed(word))
move_message = "move one from"

word = "שמאל".decode('UTF-8')
rtl_left = ''.join(reversed(word))
left = "left"

rtl_to = "ל".decode('UTF-8')
to = 'to'

word ="אֶמצַע".decode('UTF-8')
rtl_middle =''.join(reversed(word))
middle ="middle"

word = "ימין".decode('UTF-8')
rtl_right =''.join(reversed(word))
right = "right"
counter = 0;
setp_format = u"{:4d} \t {} {} {} {}"

class ring_mover:
    def __init__(self,_move_message,_to,rtl=False):
        self.move_message = _move_message
        self._to =_to
        self.rtl = rtl
        if(rtl):
            self.posts = (rtl_left,rtl_right,rtl_middle)
        else:
            self.posts = (left,right,middle)

    def move(self,f,t):
        global counter
        counter +=1
        if(self.rtl):
            print setp_format.format(counter,self.posts[t]+self._to,self.posts[f]+self.move_message,'','')
        else:
            print setp_format.format(counter, self.move_message, self.posts[f], self._to, self.posts[t])

class towers:
    def __init__(self,rtl=False):
        if(rtl):
            self._mover = ring_mover(rtl_move_message,rtl_to,rtl)

        else:
            self._mover = ring_mover(move_message,to,rtl)
            posts = (left,right,middle)

    def move(self,f,t):
        return self._mover.move(f,t)

    def towers(self,n,_from,_to,_via):
        if(1 == n):
            self.move(_from,_to)
            return
        self.towers(n-1,_from,_via,_to)
        self.move(_from,_to)
        self.towers(n-1,_via,_to,_from)
