# Component and Assembly classes

# import the 3D model
import m_model3d

class Component(object):
    """ an individual component in the assembly """
    def __init__(self, obj_file, translation):
        """ creating the component """
        # create a new 3D model for the component
        self.model3d = m_model3d.Model3D()

        # get the texture for the 3D model
        self.model3d.read_obj(obj_file)

        # translate the component to the correct space
        self.model3d.translate_object(*translation)

        # gives the object a component id, which is just the colour of the block atm
        self.component_id = obj_file[0]

        # component location is used for export info
        self.component_location = translation

    def __del__(self):
        """ deletes the 3d model to tidy up """
        del self.model3d

    def __str__(self):
        """ creates a string output for the component """
        message = self.component_id + str(self.component_location)
        return message

    def render_component(self):
        """ renders the 3d model """
        self.model3d.draw_quick()

class Joint(object):
    """ a class to hold the individual joins, hoping this makes it easier """
    def __init__(self, joint_type, location):
        self.joint_type = joint_type
        self.joint_location = location

    def __str__(self):
        """ creates a string output for the join """
        message = self.joint_type + str(self.joint_location)
        return message

class Assembly(object):
    """ the whole assembly """
    def __init__(self, component_no):
        """ creating an empty assembly """
        # setting the max number of components
        self.MAX_COMPONENTS = component_no

        # starting the work at the beginning
        self.working_position = 0

        # creating an empty dictionary of components
        self.components = {}
        for i in range(self.MAX_COMPONENTS):
            self.components[i] = None

        # creating an empty dictionary of joints
        self.joins = {}
        for i in range(self.MAX_COMPONENTS - 1):
            self.joins[i] = None
        

    def get_max_components(self):
        """ returns the maximum number of components in the assembly """
        return self.MAX_COMPONENTS

    def get_working_position(self):
        """ returns the current working position """
        return self.working_position

    def add_component(self, obj_file):
        """ adds a new component at the working position """
        # add a new component
        self.components[self.working_position] = Component(obj_file, (0, self.working_position, 0))

        # increment the working position by 1 so we know where we're at
        self.working_position += 1

    def delete_component(self):
        """ deletes the object at the current working position """
        del self.components[self.working_position-1]
        if self.working_position >= 2:
            del self.joins[self.working_position-2]
        self.working_position -= 1

    def render_components(self):
        """ renders all the components """
        for component in self.components:
            if self.components[component] is not None:
                self.components[component].render_component()

    def room_for_more(self):
        """ checks if theres room for more components in the assembly """
        return self.working_position+1 <= self.MAX_COMPONENTS

    def need_join(self):
        """ checks if a join is needed """
        # only need a join for the first and second blocks
        if self.working_position-1 == 0 or self.working_position-1 == 1:
            return True

    def set_joint(self, joint):
        """ keeps details of the joint types """
        self.joins[self.working_position-1] = Joint(joint, (0, self.working_position-1, 0))

    def ready_to_export(self):
        """ checks if the assembly is ready to export """
        ready_to_export = True

        # check to see we have 3 components that exist
        if len(self.components) == 3: # check for 3 components
            for component in self.components:
                if self.components[component] is None: # check all the components exist
                    ready_to_export = False
        else:
            ready_to_export = False

        # if we failed the component test, we dont need to look for joints
        if ready_to_export:
            if len(self.joins) == 2: # check for 2 joints
                for joint in self.joins:
                    if self.joins[joint] is None: # check all the joints exist
                        ready_to_export = False
            else:
                ready_to_export = False

        # if we passed all the checks with flying colours we cann go ahead and export
        return ready_to_export

    def create_save_file(self, filename):
        """ returns the assembly as a string to be saved """
        component_keys = list(self.components.keys())
        output = []
        for i in range(len(self.components)):
            output.append((str(self.components[component_keys[i]]) + "\n"))
            if i < self.MAX_COMPONENTS - 1:
                output.append((str(self.joins[i]) + "\n"))

        if filename[-4:].lower() != ".txt":
            filename += ".txt"

        text_file = open(filename, "w")
        text_file.writelines(output)
        text_file.close()

            
            
