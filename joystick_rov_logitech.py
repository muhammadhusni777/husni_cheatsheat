import pygame
import paho.mqtt.publish as publish
import time

a=0

axis_x_val = 0
axis_y_val = 0
axis_yaw_val = 0

message_time = 0
prev_message_time = 0

pygame.init()

# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
'''
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)
        

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, "black")
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height
        
        

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        global a
        self.x += 10
        
        a += 1
        print(a)
        if a > 50:
            a = 0
         #   print(axis_x_val)
            publish.single(u"axis x", str(axis_x_val), hostname="127.0.0.1")            
            publish.single(u"axis y", str(axis_y_val), hostname="127.0.0.1")
            publish.single(u"axis yaw", str(axis_yaw_val), hostname="127.0.0.1")

    def unindent(self):
        self.x -= 10

'''
def main():
    
    
    # Set the width and height of the screen (width, height), and name the window.
    #screen = pygame.display.set_mode((300, 370))
    #pygame.display.set_caption("ROV JOYSTICK CONTROL")

    clock = pygame.time.Clock()

    # Get ready to print.
    ##text_print = TextPrint()

    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks = {}

    done = False
    while not done:
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.

            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.")
                if event.button == 0:
                    joystick = joysticks[event.instance_id]
                    if joystick.rumble(0, 0.7, 500):
                        print(
                            "Rumble effect played on joystick {}".format(
                                event.instance_id
                            )
                        )

            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.")

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print("Joystick {} connencted".format(joy.get_instance_id()))
                

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print("Joystick {} disconnected".format(event.instance_id))

        # Drawing step
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        #screen.fill("white")
        ##text_print.reset()

        ##text_print.tprint(screen, "Number of joysticks: {}".format(len(joysticks)))
        ##text_print.indent()

        # For each joystick:
        for joystick in joysticks.values():
            global message_time
            global prev_message_time
            global axis_x_val
            global axis_y_val
            global axis_yaw_val
            
            message_time = time.time() - prev_message_time
            #print(message_time)
            if message_time > 0.5:
                print(str(round(axis_x_val,1)) + " | " +str(round(axis_y_val,1)) + " | " + str(round(axis_yaw_val,1)))
                publish.single(u"axis x", str(round(axis_x_val,1)), hostname="127.0.0.1")            
                publish.single(u"axis y", str(round(axis_y_val,1)), hostname="127.0.0.1")
                publish.single(u"axis yaw", str(round(axis_yaw_val,1)), hostname="127.0.0.1")
                prev_message_time = time.time()
            
            jid = joystick.get_instance_id()
            ##text_print.tprint(screen, "Joystick : " + "123.45.0.1".format(jid))
            ##text_print.indent()

            # Get the name from the OS for the joystick.
            name = joystick.get_name()
            ##text_print.tprint(screen, "Joystick name: {}".format(name))

            guid = joystick.get_guid()
            ##text_print.tprint(screen, "GUID: {}".format(guid))

            power_level = joystick.get_power_level()
            ##text_print.tprint(screen, "Joystick's power level: {}".format(power_level))

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other. Triggers count as axes.
            axes = joystick.get_numaxes()
            #text_print.tprint(screen, "Number of axes: {}".format(axes))
            #text_print.indent()

            for i in range(axes):
                
                axis = joystick.get_axis(i)
                #text_print.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis))
                #print(str(i) + " " + str(axis))
                if i == 0 :
                    axis_x_val = axis
                if i == 1 :
                    axis_y_val = axis

                if i == 2 :
                    axis_yaw_val = axis
                
                a =+ 1
                #print(a)
                
                
                
                
                
                
            #text_print.unindent()

            buttons = joystick.get_numbuttons()
            #text_print.tprint(screen, "Number of buttons: {}".format(buttons))
            #text_print.indent()

            for i in range(buttons):
                button = joystick.get_button(i)
                #text_print.tprint(screen, "Button {:>2} value: {}".format(i, button))
            #text_print.unindent()

            hats = joystick.get_numhats()
            #text_print.tprint(screen, "Number of hats: {}".format(hats))
            #text_print.indent()

            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).
            for i in range(hats):
                hat = joystick.get_hat(i)
                #text_print.tprint(screen, "Hat {} value: {}".format(i, str(hat)))
            #text_print.unindent()

            #text_print.unindent()

        # Go ahead and update the screen with what we've drawn.
        #pygame.display.flip()

        # Limit to 30 frames per second.
        clock.tick(30)





    
    
if __name__ == "__main__":
    main()
    
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()

