# LIPGLOSS - Graphical user interface for constructing glaze recipes
# Copyright (C) 2017 Pieter Mostert

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# version 3 along with this program (see LICENCE.txt).  If not, see
# <http://www.gnu.org/licenses/>.

# Contact: pi.mostert@gmail.com

# We define the Restriction, Oxide, Ingredient,and Other classes.

from tkinter import *
from view.pretty_names import prettify
from functools import partial
import shelve
import copy

from pulp import *

# SECTION 1
# Define Restriction class

class Restriction:
    'Oxide UMF, oxide % molar, oxide % weight, ingredient, SiO2:Al2O3 molar, LOI, cost, etc'
    #display_frame = None
    
    def __init__(self, index, name, objective_func, normalization, default_low, default_upp, dec_pt=1):

        self.index = index     # We will always have restr_dict[index] = Restriction(frame, index, ...)
        self.name = name
        self.objective_func = objective_func
        self.normalization = normalization
        self.default_low = default_low
        self.default_upp = default_upp
        self.dec_pt = dec_pt
        
        self.calc_bounds = {}   

    def remove(self, recipe):
        for widget in [self.left_label, self.lower_bound, self.upper_bound, self.calc_bounds[-1], self.calc_bounds[1],
                       self.right_label]:
            widget.grid_forget()    # remove widgets corresponding to that restriction
        self.low.set(self.default_low)
        self.upp.set(self.default_upp)
        for eps in [-1, 1]:
            self.calc_bounds[eps].config(text='')
        v = dict(recipe.variables)
        for t in v:
            if self.index == v[t]:
                self.deselect(t)
                del recipe.variables[t]

    def hide(self):  # to be used with oxide options
        for widget in [self.left_label, self.lower_bound, self.upper_bound, self.calc_bounds[-1], self.calc_bounds[1],
                       self.right_label]:
            widget.grid_forget()

    def display_calc_bounds(self):
        for eps in [-1, 1]:
            self.calc_bounds[eps].config(text=('%.' + str(self.dec_pt) + 'f') % self.calc_value[eps])


# SECTION 3
#
# Define Other_Attribute class and initialize other attributes
##
##class Other_Attribute:
##    
##     def __init__(self, name, pos):
##         'LOI, cost, clay, etc'
##
##         self.name = name
##         self.pos = pos  # Determines order in which other attributes are displayed.
##
### Once users are able to add their own attributes, other_attr_dict will be determined by the entries in
### OtherAttributeShelf (yet to be defined).  For now we just do things manually.
##other_attr_dict = {}     
##other_attr_dict['0'] = Other_Attribute('LOI', 0)
##other_attr_dict['1'] = Other_Attribute('cost', 1)
##other_attr_dict['2'] = Other_Attribute('clay', 2)


# SECTION 4
###
### Define Ingredient class.  Ingredients will be referenced by their index, a string consisting of a unique natural number.
##class Ingredient:    
##    
##    def __init__(self, name='New ingredient', notes='', oxide_comp={}, other_attributes={}):
##
##        self.name = name
##        # notes not implemented yet. Intended to show up in the 'Edit ingredients' window.
##        self.notes = notes
##        # oxide_comp is a dictionary giving the weight percent of each oxide in the ingredient.
##        self.oxide_comp = oxide_comp  
##        self.other_attributes = other_attributes
##        self.display_widgets = {}
##
##    def displayable_version(self, index, frame, delete_ingredient_fn):
##        # To be used in the 'Edit ingredients' window.  Only apply this to copies of things in shelve.
##        sdw = self.display_widgets
##        sdw['del'] =  ttk.Button(master=frame, text='X', width=2, command = partial(delete_ingredient_fn, index))
####        sdw['del'] =  ttk.Label(master=frame, text='X', width=2)
####        sdw['del'].bind('<Button-1>', partial(delete_ingredient_fn, index))
##        sdw['name'] = Entry(master=frame, width=20)
##        sdw['name'].insert(0, self.name)
##
##        c = 3
##        
##        for ox in oxides:
##            # Use this entry widget to input the percent weight of the oxide that the ingredient contains.
##            sdw[ox] = Entry(master=frame,  width=5)  
##            sdw[ox].delete(0, END)
##            if ox in self.oxide_comp:
##                sdw[ox].insert(0, self.oxide_comp[ox])
##            else:
##                pass
##            c += 1
##
##        for i, other_attr in other_attr_dict.items(): 
##            sdw['other_attr_'+i] = Entry(master=frame, width=5)
##            if i in self.other_attributes:
##                sdw['other_attr_'+i].insert(0, self.other_attributes[i])
##
##    def display(self, pos):
##        sdw = self.display_widgets
##        sdw['del'].grid(row=pos, column=0)
##        sdw['name'].grid(row=pos, column=1, padx=3, pady=3)
##
##        c = 3
##        
##        for ox in oxides:
##            sdw[ox].grid(row=pos, column=c, padx=3, pady=1)
##            c += 1
##
##        for i, other_attr in other_attr_dict.items(): 
##            sdw['other_attr_'+i].grid(row=pos, column=c+other_attr.pos, padx=3, pady=3)
##
##    def pickleable_version(self):   
##        temp = copy.copy(self)
##        # The values in self.display_widgets that the ingredient editor introduces can't be pickled, so we discard them:
##        temp.display_widgets = {}    
##        return temp

# SECTION 5
#
# Define Other class



# SECTION 6 (move to GUI)
#
# Initialize the restr_dict, oxide_dict, ingredient_dict, and other_dict dictionaries.
# Define default recipe bounds (optional).
# Set up the linear programming problem. Define variables, and set constraints that always hold (unless any
# of the dictionaries above are modified).

# restr_dict is a dictionary with keys of the form 'umf_'+ox, 'mass_perc_'+ox, 'mole_perc_'+ox, 'ingredient_'+index or 'other_'+index.
##restr_dict = {}  
##
##with shelve.open("./data/OxideShelf") as oxide_shelf:
##    # Create oxide restrictions.
##    for ox in oxide_shelf:   
##        def_upp = 1   # Default upper bound for oxide UMF.
##        dp = 3
##        if ox == 'SiO2':
##            def_upp = 100
##            dp = 2
##        elif ox == 'Al2O3':
##            def_upp = 10
##        restr_dict['umf_'+ox] = Restriction(restriction_sf.interior,'umf_'+ox, ox, 'mole_'+ox, "lp_var['fluxes_total']", 0, def_upp, dec_pt=dp)
##        restr_dict['mass_perc_'+ox] = Restriction(restriction_sf.interior,'mass_perc_'+ox, ox, 'mass_'+ox, "0.01*lp_var['ox_mass_total']", 0, 100, dec_pt=2) 
##        restr_dict['mole_perc_'+ox] = Restriction(restriction_sf.interior,'mole_perc_'+ox, ox, 'mole_'+ox, "0.01*lp_var['ox_mole_total']", 0, 100, dec_pt=2)
##
### If there are a large number of ingredients, maybe it's better to only create
### the corresponding restrictions once they're selected for a particular recipe.
##        
##if initialize_ingredients == 1:
##    from data import ingredientfile
##        
##    with shelve.open("./data/IngredientShelf") as ingredient_shelf:
##        for index in ingredient_shelf:
##            del ingredient_shelf[index]
##
##        temp_order_list = []
##        for (pos, ing) in enumerate(ingredientfile.ingredient_names):
##
##            temp_order_list.append(str(pos))
##
##            ing_init = Ingredient(name=ing, oxide_comp=dict([(ox, ingredientfile.ingredient_compositions[ing][ox]) \
##                                                                   for ox in oxides if ox in ingredientfile.ingredient_compositions[ing]]),\
##                                  other_attributes = {})
##
##            for attr in other_attr_dict:
##                try:
##                    ing_init.other_attributes[attr] = ingredientfile.ingredient_compositions[ing][attr]
##                except:
##                    pass
##                    
##            ingredient_shelf[str(pos)] = ing_init
##
##    with shelve.open("./data/OrderShelf") as order_shelf:
##        order_shelf['ingredients'] = temp_order_list
##        
##else:
##    pass
##
##with shelve.open("./data/IngredientShelf") as ingredient_shelf:   
##
##    # This is defined again in GUI.py. Need to rethink.
##    ingredient_dict = dict(ingredient_shelf)
##    
##    for index in ingredient_shelf:
##        restr_dict['ingredient_'+index] = Restriction(restriction_sf.interior,'ingredient_'+index, ingredient_shelf[index].name, 'ingredient_'+index, "0.01*lp_var['ingredient_total']", 0, 100)
##
##if True:
##    with shelve.open("./data/OtherShelf") as other_shelf:
##        for index in other_shelf:
##            del other_shelf[index]
##        other_shelf['0'] = Other(0,'SiO2_Al2O3', {'mole_SiO2':1}, "lp_var['mole_Al2O3']", 3, 18, 2)   # Using 'SiO2:Al2O3' gives an error
##        other_shelf['1'] = Other(1,'KNaO UMF', {'mole_K2O':1, 'mole_Na2O':1}, "lp_var['fluxes_total']", 0, 1, 3)
##        other_shelf['2'] = Other(2,'KNaO % mol', {'mole_K2O':1, 'mole_Na2O':1}, "0.01*lp_var['ox_mole_total']", 0, 100, 1)
##        other_shelf['3'] = Other(3,'RO UMF', {'mole_MgO':1, 'mole_CaO':1, 'mole_BaO':1, 'mole_SrO':1}, "lp_var['fluxes_total']", 0, 1, 3)
##
##        other_att_4 = {'ingredient_'+index : 0.01*float(ingredient_dict[index].other_attributes['2']) for index in ingredient_dict if '2' in ingredient_dict[index].other_attributes}
##        other_shelf['4'] = Other(4,'Total clay', {k:v for k,v in other_att_4.items() if v>0}, "0.01*lp_var['ingredient_total']", 0, 100, 1)
##        other_att_5 = {'ingredient_'+index : 0.01*float(ingredient_dict[index].other_attributes['0']) for index in ingredient_dict if '0' in ingredient_dict[index].other_attributes}
##        other_shelf['5'] = Other(5,'LOI',  {k:v for k,v in other_att_5.items() if v>0}, "0.01*lp_var['ingredient_total']", 0, 100, 1)
##        other_att_6 = {'ingredient_'+index : 0.01*float(ingredient_dict[index].other_attributes['1']) for index in ingredient_dict if '1' in ingredient_dict[index].other_attributes}
##        other_shelf['6'] = Other(6,'cost', {k:v for k,v in other_att_6.items() if v>0}, "0.01*lp_var['ingredient_total']", 0, 100, 1)
##        
##        other_dict = dict(other_shelf)
##else:
##    other_dict = update_other()
##    
##with shelve.open("./data/OtherShelf") as other_shelf:
##    for index in other_shelf:
##        ot = other_shelf[index]    # instance of 'Other' class
##        restr_dict['other_'+index] = Restriction(restriction_sf.interior,'other_'+index, ot.name, 'other_'+index, ot.normalization, ot.def_low, ot.def_upp, dec_pt=ot.dec_pt)
##
###Initialize oxides:  
##
##if initialize_oxides == 1:
##    from data import oxidefile
##
##    with shelve.open("./data/OxideShelf") as oxide_shelf:
##        for ox in oxide_shelf:
##            del oxide_shelf[ox]
##        for (pos, ox) in enumerate(oxidefile.oxides):
##            if ox in oxidefile.fluxes:
##                ox_init = Oxide(pos, molar_mass=oxidefile.molar_mass_dict[ox], flux=1)
##            else:
##                ox_init = Oxide(pos, molar_mass=oxidefile.molar_mass_dict[ox], flux=0)
##            oxide_shelf[ox] = ox_init
##else:
##    pass
##
##def update_ox():
##    global oxides
##    global molar_masses
##    with shelve.open("./data/OxideShelf") as oxide_shelf:
##        oxides = [ox for ox in oxide_shelf]
##        molar_masses = {ox:oxide_shelf[ox].molar_mass for ox in oxide_shelf}
##        return dict(oxide_shelf)
##    
##oxide_dict = update_ox()
##
### Define ingredients.
##
##def update_ing():
##    with shelve.open("./data/IngredientShelf") as ingredient_shelf:
##        return dict(ingredient_shelf)
##
##if initialize_ingredients == 1:
##    from data import ingredientfile
##        
##    with shelve.open("./data/IngredientShelf") as ingredient_shelf:
##        for index in ingredient_shelf:
##            del ingredient_shelf[index]
##
##        temp_order_list = []
##        for (pos, ing) in enumerate(ingredientfile.ingredient_names):
##
##            temp_order_list.append(str(pos))
##
##            ing_init = Ingredient(name=ing, oxide_comp=dict([(ox, ingredientfile.ingredient_compositions[ing][ox]) \
##                                                                   for ox in oxides if ox in ingredientfile.ingredient_compositions[ing]]),\
##                                  other_attributes = {})
##
##            for attr in other_attr_dict:
##                try:
##                    ing_init.other_attributes[attr] = ingredientfile.ingredient_compositions[ing][attr]
##                except:
##                    pass
##            
##            ingredient_shelf[str(pos)] = ing_init
##
##    with shelve.open("./data/OrderShelf") as order_shelf:
##        order_shelf['ingredients'] = temp_order_list
##        
##else:
##    pass
##
##ingredient_dict = update_ing()
##
##with shelve.open("./data/OrderShelf") as order_shelf:
##    ingredient_order = order_shelf['ingredients']
##
##def get_ing_comp(ingredient_dict):
##    ingredient_compositions = {}
##    for index in ingredient_dict:
##        ingredient_compositions[index] = ingredient_dict[index].oxide_comp
##    return ingredient_compositions
##
##ingredient_compositions = get_ing_comp(ingredient_dict)
##
### Initialize other.
##
##def update_other():
##    with shelve.open("./data/OtherShelf") as other_shelf:
##        other_dict = dict(other_shelf)
##        return other_dict
##        
##other_dict = update_other()
##
##
