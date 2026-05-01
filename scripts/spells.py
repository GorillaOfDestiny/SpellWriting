"""Aim is to create a class that contains all the useful
functions a spell might need
    """
import matplotlib.pyplot as plt #There's almost certainly a better way than matplotlib but oh well
import numpy as np
from collections.abc import Callable
from necklaces import default_generation
import os
import bases
import line_shapes
class custom_spell_input():
    """Class for custom inputting of spell data. Usually use the argparse object but this lets you do it in a code way
    """
    def __init__(self,
                 level,
                 school,
                damagetype,
                 aoe,
                 range,
                 duration,
                 concentration = False,
                 ritual = False,
                 spell_name = "Test"):
        """Initialisation of class.

        Args:
            level (str): Spell level
            school (str): School of spell
            damagetype (str): Damage type of Spell
            aoe (str): Area of Effect of Spell
            range (str): Range of Spell
            duration (str): Duration of Spell
            concentration (bool, optional): bool for whether spell is concentration. Defaults to False.
            ritual (bool, optional): bool for whether spell is ritual. Defaults to False.
        """
        self.level = str(level).lower()
        self.school = school.lower()
        self.damagetype = damagetype.lower()
        self.aoe = aoe.lower()
        self.range = range.lower()
        self.duration = duration.lower()
        self.concentration = concentration
        self.ritual = ritual
        self.spell_name = spell_name

class spell():
    def __init__(self,input_obj: custom_spell_input,base_fn:Callable=bases.polygon,
                 line_fn:Callable = line_shapes.straight,
                 txt_file_base:str = r"./attribute_ordering/",
                 n_att = None,
                 n_pol = None,
                 override_dict = {},
                 base_kwargs = [],
                 line_kwargs = [],
                 ignore_atts = False):
        self.__name__ = input_obj.spell_name
        self.ignore_atts = ignore_atts
        self.atts = ["level","school","damagetype",
                     "aoe","range","duration",
                     "concentration","ritual"]

        self.level = input_obj.level.lower()
        self.school = input_obj.school.lower()
        self.damagetype = input_obj.damagetype.lower()
        self.aoe = input_obj.aoe.lower()
        self.range = input_obj.range.lower()
        self.duration = input_obj.duration.lower()
        self.concentration = input_obj.concentration
        self.ritual = input_obj.ritual
        self.att_strs = [self.level,self.school,self.damagetype,self.aoe,self.range,self.duration,
                         self.concentration,self.ritual]
        
        self.base_fn = base_fn
        self.base_kwargs = base_kwargs
        self.line_fn = line_fn
        self.line_kwargs = line_kwargs
        if not self.ignore_atts:
            #skip this if ignoring_atts since we won't need it
            self.init_txt_files(txt_file_base)

            if n_att is None:
                self.n_att = len(self.txt_files)
            if n_pol is None:
                self.n_pol = 2*self.n_att + 1
            for i in range(len(self.txt_files)):
                assert os.path.isfile(self.txt_files[i]), f"Could not find file {self.txt_files[i]}"
            self.get_binary_values(override_dict)
        else:
            self.n_att = n_att
            self.n_pol = n_pol
        

    def init_txt_files(self,txt_file_base):
        self.txt_file_base = txt_file_base
        self.aoe_txt_file = os.path.join(self.txt_file_base, r"area_types.txt")
        self.dmg_txt_file = os.path.join(self.txt_file_base,r"damage_types.txt")
        self.dur_txt_file = os.path.join(self.txt_file_base,r"duration.txt")
        self.lvl_txt_file = os.path.join(self.txt_file_base,r"levels.txt")
        self.ran_txt_file = os.path.join(self.txt_file_base,r"range.txt")
        self.sch_txt_file = os.path.join(self.txt_file_base,r"school.txt")
        self.txt_files = [self.lvl_txt_file,
                          self.sch_txt_file,
                          self.dmg_txt_file,
                          self.aoe_txt_file,
                          self.ran_txt_file,
                          self.dur_txt_file]
        
    def read_txt_file(self,fpath):
        with open(fpath,"r") as f:
            data = f.readlines()
            f.close()
        data = [d.replace("\n","").lower() for d in data]
        return(data)
    def get_decimal_values(self,override_dict = {}):
        decimal_array = np.zeros(self.n_att)
        override_keys = list(override_dict.keys())
        for i in range(self.n_att):
            if self.atts[i] in override_keys:
                decimal_array[i] = override_dict[self.atts[i]]
            else:
                att_items = self.read_txt_file(self.txt_files[i])
                idx = att_items.index(self.att_strs[i])
                decimal_array[i] = idx
        return(decimal_array)
    def get_binary_values(self,override_dict = {}):
        binary_values = default_generation()
        self.binary_array = np.zeros((self.n_att,self.n_pol),dtype = int)
        override_keys = list(override_dict.keys())
        for i in range(self.n_att):
            if self.atts[i] in override_keys:
                self.binary_array[i] = override_dict[self.atts[i]]
            else:
                att_items = self.read_txt_file(self.txt_files[i])
                idx = att_items.index(self.att_strs[i])
                self.binary_array[i] = binary_values[idx]
        
        #------hard coding in the binary attributes
        self.level_b = binary_values[0]
        self.school_b = binary_values[1]
        self.damagetype_b = binary_values[2]
        self.aoe_b = binary_values[3]
        self.range_b = binary_values[4]
        self.duration_b = binary_values[5]

    def draw(self,annotate = False,
             show_all_paths = False,
             savename = "output.png",
             output_dpi = 200,
             axs = None,
             dot_color = 'k',
             cmap = 'magma',
             line_color = 'darkred',
             dot_size = 50,
             legend_fontsize = 10,
             legend_anchor = (1,0.75),
             show_name = False):
        assert self.n_pol == self.binary_array.shape[1]
        assert self.n_att == self.binary_array.shape[0]
        cmap = plt.get_cmap(cmap)
        x_vals,y_vals = self.base_fn(self.n_pol,*self.base_kwargs)

        if axs is None:
            fig,axs = plt.subplots(1,1)
        else:
            fig = plt.gcf()
        axs.set_aspect('equal')
        
        #draw the points
        axs.scatter(x_vals[0],y_vals[0],color = dot_color,marker = "o",s = dot_size)
        axs.scatter(x_vals[1:],y_vals[1:],color = dot_color,marker = "o",s = dot_size,facecolors = 'none')

        if show_all_paths:
            self.draw_all_paths(x_vals,y_vals,axs)

        for i in range(self.n_att):
            k = i + 1
            if annotate:
                color = cmap(0.9*i/(self.n_att))
            else:
                color = line_color
            labelled = False
            for j,elem in enumerate(self.binary_array[i]):
                
                if elem == 1:
                    #if element is 1
                    P = [x_vals[j],y_vals[j]]
                    Q = [x_vals[(j+k)%self.n_pol],y_vals[(j+k)%self.n_pol]]
                    line_x,line_y = self.line_fn(P,Q,*self.line_kwargs)
                    
                    axs.plot(line_x,line_y,
                             ls = "-",
                             lw = 2,
                             color = color,
                             label = self.att_strs[i] if (labelled is False) and annotate == True else None,
                             zorder = 0)
                    labelled = True
        if self.concentration:
            axs.plot(0,0,"",markersize = 10,marker = ".",color = dot_color)
        if self.ritual:
            axs.plot(0,0,"",markersize = 20,marker = "o",color=dot_color,mfc='none',linewidth = 20)
        if annotate:
            axs.legend(fontsize = legend_fontsize,bbox_to_anchor = legend_anchor)
        #save_figure
        axs.set_axis_off()
        if show_name:
            axs.set_title(self.__name__)
        if savename is not None:
            plt.savefig(savename,dpi = output_dpi,bbox_inches = 'tight')
        else:
            plt.show()



    def draw_all_paths(self,x_vals,y_vals,axs,
                       all_ls = "--",all_c = 'k',all_alpha = 0.7,all_lw = 0.5):
        #loop for all k
        for k in range(1,self.n_att+1):
            for i in range(self.n_pol):
                P = [x_vals[i],y_vals[i]]
                Q = [x_vals[(i+k)%self.n_pol],y_vals[(i+k)%self.n_pol]]
                line_x,line_y = self.line_fn(P,Q,*self.line_kwargs)
                axs.plot(line_x,line_y,
                         ls = all_ls,
                         color = all_c,
                         alpha = all_alpha,
                         lw = all_lw)
                
if __name__ == "__main__":
    test_inp = custom_spell_input(3,"evocation",
                                  "fire","sphere (20)",
                                  "150 feet","Instantaneous",
                                  spell_name="")
    # test_obj = spell(test_inp,
    #                  bases.polygon,
    #                  base_kwargs = [],
    #                  line_fn = line_shapes.straight,
    #                  line_kwargs = [])
    test_obj = spell(test_inp,ignore_atts=True,
                     n_pol = 5,n_att = 2,
                     base_kwargs = [1,-2*np.pi/5])
    
    test_obj.binary_array = np.zeros((test_obj.n_att,test_obj.n_pol))
    test_obj.binary_array[0] = np.array([0,0,0,0,1])
    test_obj.draw(savename = None,show_all_paths=True,annotate=False,
                  show_name=True)
    
    