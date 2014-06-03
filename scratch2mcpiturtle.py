#!/usr/bin/env python

import sys
import os
import gettext
import scratch
import mcpi.minecraft as minecraft
import minecraftturtle
import block
import time

VERSION = "1.0.3a"
localedir = os.path.join(os.path.dirname(__file__), 'locale')
_ = gettext.translation(domain = 'scratch2mcpi', localedir = localedir, fallback = True).ugettext

def is_number(mc, variable_name, value):
  if (isinstance(value, (int, float))):
    return True
  else:
    return False

def connect():
  try:
    return scratch.Scratch()
  except scratch.ScratchError:
    print _("Error: Unable to connect to Scratch. Scratch may be not running or the remote sensor connections may be not enabled.") 
    return None

def _listen(s):
  while True:
    try:
      yield s.receive()
    except scratch.ScratchError:
      print _("Error: Disconnected from Scratch.")
      raise StopIteration

def listen(s, mc):
  mcpiX = 0
  mcpiY = 0
  mcpiZ = 0
  mcpiX0 = 0
  mcpiY0 = 0
  mcpiZ0 = 0
  mcpiX1 = 0
  mcpiY1 = 0
  mcpiZ1 = 0
  blockTypeId = 1
  blockData = 0
  # Minecraft Graphics Turtle(Start)
  forward = 0
  backward = 0
  right = 0
  left = 0
  up = 0
  down = 0
  speed = 10
  turtleX = 0
  turtleY = 0
  turtleZ = 0
  penBlockId = block.DIRT.id
  penBlockData = 0
  mc = minecraft.Minecraft.create()
  pos = mc.player.getPos()
  steve = minecraftturtle.MinecraftTurtle(mc,pos)
  spos = steve.position
  # Minecraft Graphics Turtle(End)

  for msg in _listen(s):
    if (msg):
      print "Received: %s" % str(msg)
      if msg[0] == 'broadcast':
        if not mc:
          mc = minecraft.Minecraft.create()
        if msg[1] == 'hello_minecraft':
          mc.postToChat("hello minecraft")
        elif msg[1] == 'setPos':
          if (is_number(mc, "mcpiX", mcpiX) and is_number(mc, "mcpiY", mcpiY) and is_number(mc, "mcpiZ", mcpiZ)): 
            mc.player.setPos(mcpiX, mcpiY, mcpiZ)
            print "setPos: %.1f %.1f %.1f" % (mcpiX, mcpiY, mcpiZ)
        elif msg[1] == 'setBlock':
          if (is_number(mc, 'mcpiX', mcpiX) and is_number(mc, 'mcpiY', mcpiY) and is_number(mc, 'mcpiZ', mcpiZ) and is_number(mc, 'blockTypeId', blockTypeId) and is_number(mc, 'blockData', blockData)):
            mc.setBlock(mcpiX, mcpiY, mcpiZ, blockTypeId, blockData)
            print "setBlock: %d %d %d %d %d" % (mcpiX, mcpiY, mcpiZ, blockTypeId, blockData)
        # Minecraft Graphics Turtle(Start)
	elif msg[1] == 'initTurtle':
            steve = minecraftturtle.MinecraftTurtle(mc,spos)
	    print "steve.__init__"
        elif msg[1] == 'setPosTurtle':
          if (is_number(mc, "turtleX", turtleX) and is_number(mc, "turtleY", turtleY) and is_number(mc, "turtleZ", turtleZ)): 
            # steve.setposition(turtleX, turtleY, turtleZ)
            steve.setx(turtleX)
            steve.sety(turtleY)
            steve.setz(turtleZ)
            print "setpositionTurtle: %.1f %.1f %.1f" % (turtleX, turtleY, turtleZ)
	elif msg[1] == 'setForward':
          if is_number(mc, 'forward', forward) :
	    steve.forward(forward)          		  
	    print "steve.forward: (%d)" % (forward)
	elif msg[1] == 'setBackward':
          if is_number(mc, 'backward', backward) :
	    steve.backward(backward)          		  
	    print "steve.backward: (%d)" % (backward)
	elif msg[1] == 'setRight':
          if is_number(mc, 'right', right) :
	    steve.right(right)          		  
	    print "steve.right: (%d)" % (right)
	elif msg[1] == 'setLeft':
          if is_number(mc, 'left', left) :
	    steve.left(left)          		  
	    print "steve.left: (%d)" % (left)
	elif msg[1] == 'setUp':
          if is_number(mc, 'up', up) :
	    steve.up(up)          		  
	    print "steve.up: (%d)" % (up)
	elif msg[1] == 'setDown':
          if is_number(mc, 'down', down) :
	    steve.down(down)          		  
	    print "steve.down: (%d)" % (down)
	elif msg[1] == 'setSpeed':
          if is_number(mc, 'speed', speed) :
	    steve.speed(speed)          		  
	    print "steve.speed: (%d)" % (speed)
	elif msg[1] == 'setPenBlockId':
	    steve.penblock(penBlockId)          		  
	    print "steve.penblock: (%s)" % (penBlockId)
	elif msg[1] == 'setPenBlockData':
	    steve.penblock(penBlockId, penBlockData)          		  
	    print "steve.penblock: (%s, %d)" % (penBlockId, penBlockData)
        # Minecraft Graphics Turtle(End)
	elif msg[1] == 'setBlocks':
          if (is_number(mc, 'mcpiX0', mcpiX0) and is_number(mc, 'mcpiY0', mcpiY0) and is_number(mc, 'mcpiZ0', mcpiZ0) and is_number(mc, 'mcpiX1', mcpiX1) and is_number(mc, 'mcpiY1', mcpiY1) and is_number(mc, 'mcpiZ1', mcpiZ1) and is_number(mc, 'blockTypeId', blockTypeId) and is_number(mc, 'blockData', blockData)):
            mc.setBlocks(mcpiX0, mcpiY0, mcpiZ0, mcpiX1, mcpiY1, mcpiZ1, blockTypeId, blockData)
            print "setBlocks(%d, %d, %d, %d, %d, %d, %d, %d" % (mcpiX0, mcpiY0, mcpiZ0, mcpiX1, mcpiY1, mcpiZ1, blockTypeId, blockData)
        elif msg[1] == 'getPos':
          playerPos = mc.player.getPos()
	  pos = playerPos
          s.sensorupdate(
           {'playerX': playerPos.x,
            'playerY': playerPos.y,
            'playerZ': playerPos.z}
          )
        elif msg[1] == 'getHeight':
          posY = mc.getHeight(mcpiX, mcpiZ)
          s.sensorupdate({'posY': posY})
          mc.postToChat("posY: %d" % posY)
        elif msg[1] == 'pollBlockHits':
          blockEvents = mc.events.pollBlockHits()
          print blockEvents
          if blockEvents:
            blockEvent = blockEvents[-1]
            s.sensorupdate(
             {'blockEventX': blockEvent.pos.x,
              'blockEventY': blockEvent.pos.y,
              'blockEventZ': blockEvent.pos.z,
              'blockEventFace': blockEvent.face,
              'blockEventEntityId': blockEvent.entityId}
            )
          else:
            s.sensorupdate(
             {'blockEventX': '',
              'blockEventY': '',
              'blockEventZ': '',
              'blockEventFace': '',
              'blockEventEntityId': ''}
            )
        elif msg[1] == 'reset':
          mc.postToChat('reset the world')
          mc.setBlocks(-100, 0, -100, 100, 63, 100, 0, 0)
          mc.setBlocks(-100, -63, -100, 100, -2, 100, 1, 0)
          mc.setBlocks(-100, -1, -100, 100, -1, 100, 2, 0)
          mc.player.setPos(0, 0, 0)
      elif msg[0] == 'sensor-update':
        mcpiX = msg[1].get('mcpiX', mcpiX)
        mcpiY = msg[1].get('mcpiY', mcpiY)
        mcpiZ = msg[1].get('mcpiZ', mcpiZ)
        mcpiX0 = msg[1].get('mcpiX0', mcpiX0)
        mcpiY0 = msg[1].get('mcpiY0', mcpiY0)
        mcpiZ0 = msg[1].get('mcpiZ0', mcpiZ0)
        mcpiX1 = msg[1].get('mcpiX1', mcpiX1)
        mcpiY1 = msg[1].get('mcpiY1', mcpiY1)
        mcpiZ1 = msg[1].get('mcpiZ1', mcpiZ1)
        blockTypeId = msg[1].get('blockTypeId', blockTypeId)
        blockData = msg[1].get('blockData', blockData)
        # Minecraft Graphics Turtle(Start)
        forward = msg[1].get('forward', forward)
        backward = msg[1].get('backward', backward)
        right = msg[1].get('right', right)
        left = msg[1].get('left', left)
        up = msg[1].get('up', up)
        down = msg[1].get('down', down)
        speed = msg[1].get('speed', speed)
        turtleX = msg[1].get('turtleX', turtleX)
        turtleY = msg[1].get('turtleY', turtleY)
        turtleZ = msg[1].get('turtleZ', turtleZ)
        penBlockId = msg[1].get('penBlockId', penBlockId)
        penBlockData = msg[1].get('penBlockData', penBlockData)
        # Minecraft Graphics Turtle(Start)


def main():
  print "================="
  print "Sratch2MCPI %s" % VERSION
  print "================="
  print ""

  while True:
    s = connect()
    mc = minecraft.Minecraft.create()

    if (s):
      mc.postToChat("Scratch2MCPI connected to Minecraft Pi.")
      print _("Connected to Scratch")

      s.broadcast("hello_minecraft")
      s.broadcast("setPos")
      s.broadcast("setBlock")
      # s.broadcast("setBlocks")
      s.broadcast("getPos")
      s.broadcast("getHeight")
      s.broadcast("pollBlockHits")
      s.broadcast("reset")
      # Minecraft Graphics Turtle(Start)
      s.broadcast("setForward")
      s.broadcast("setBackward")
      s.broadcast("setRight")
      s.broadcast("setLeft")
      s.broadcast("setUp")
      s.broadcast("setDown")
      s.broadcast("setSpeed")
      s.broadcast("setTurtleX")
      s.broadcast("setTurtleY")
      s.broadcast("setTurtleZ")
      s.broadcast("setPosTurtle")
      s.broadcast("initTurtle")
      s.broadcast("setPenBlockId")
      s.broadcast("setPenBlockData")
      s.broadcast("penup")
      s.broadcast("pendown")
      # Minecraft Graphics Turtle(End)

      listen(s, mc)
    time.sleep(5)

main()
