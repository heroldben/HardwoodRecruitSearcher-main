import math

height_inc_dec = .1131
weight_inc_dec = .4412
wingspan_inc_dec = .1131
vertical_inc_dec = .2475


def height_pred(fresh_height):
  res = fresh_height + fresh_height * height_inc_dec
  #print(res)
  res_string = str(res)

  dec_values = res_string.split(".")[-1]
  tenths = int(dec_values[0])

  if tenths < 4:
    return math.floor(res)  #Round down .00
  if tenths >= 4 and tenths < 9:
    if tenths < 8:
      return round(res * 2) / 2 #rounds to .5
    else:
      return math.floor(res * 2) / 2 #rounds to .5
  else:
    return math.ceil(res)  # Round up 1.00


def weight_pred(fresh_weight):
  res = fresh_weight + fresh_weight * weight_inc_dec
  return round(res / 5) * 5  #rounds to 0 or 5


def wingspan_pred(fresh_wingspan):
  res = fresh_wingspan + fresh_wingspan * wingspan_inc_dec
  return round(res * 4) / 4  #rounds to nearest .25

def wingspan_pred_nonFresh(fresh_height,curr_height,curr_wingspan):
  pred_height = height_pred(fresh_height)
  height_progress = curr_height - fresh_height
  projected_height_inc = pred_height - fresh_height
  growth_height = height_progress / projected_height_inc

  growth_wing = growth_height * wingspan_inc_dec
  fresh_wing = curr_wingspan / (1 + growth_wing)
  
  pred_wingspan = wingspan_pred(fresh_wing)

  return pred_wingspan


def vertical_pred(fresh_vertical):
  res = fresh_vertical + fresh_vertical * vertical_inc_dec
  return round(res * 2) / 2  #rounds to neasted .5

#Finds projected vert of a non_freshman
def vertical_pred_nonFresh(fresh_height,curr_height,curr_vert):
  pred_height = height_pred(fresh_height)
  height_progress = curr_height - fresh_height
  projected_height_inc = pred_height - fresh_height
  growth_height = height_progress / projected_height_inc

  growth_vert = growth_height * vertical_inc_dec
  fresh_vert = curr_vert / (1 + growth_vert)
  pred_vertical = vertical_pred(fresh_vert)

  return pred_vertical


#Finds the freshman wingspan and vertical using current measurables
def find_fresh_measurable(fresh_height, curr_height):
  curr_wing = float(input("Current Wingspan (inches): "))
  curr_vert = float(input("Current Vertical: "))

  pred_height = height_pred(fresh_height)
  height_progress = curr_height - fresh_height
  projected_height_inc = pred_height - fresh_height
  growth_height = height_progress / projected_height_inc

  #Wingspan
  growth_wing = growth_height * wingspan_inc_dec
  fresh_wing = curr_wing / (1 + growth_wing)

  #Vertical
  growth_vert = growth_height * vertical_inc_dec

  fresh_vert = curr_vert / (1 + growth_vert)

  return fresh_wing, fresh_vert


#Parameter and Return Function
def measurable_pred(fresh_height, fresh_weight, fresh_wingspan,
                    fresh_vertical):
  pred_height = height_pred(fresh_height)
  pred_weight = weight_pred(fresh_weight)
  pred_wingspan = wingspan_pred(fresh_wingspan)
  pred_vertical = vertical_pred(fresh_vertical)
  return pred_height, pred_weight, pred_wingspan, pred_vertical


def measurable_pred_asker():
  isFresh = input("Is the player a HSFR? (y/n):")
  if "y" in isFresh.lower():
    fresh_height = float(input("Freshman Height (inches): "))
    fresh_weight = int(input("Freshman Weight (lbs): "))
    fresh_wingspan = float(input("Freshman Wingspan (inches): "))
    fresh_vertical = float(input("Freshman Vertical (inches): "))
  else:
    fresh_height = float(input("Freshman Height (inches): "))
    curr_height = float(input("Current Height (inches): "))
    fresh_weight = int(input("Freshman Weight (lbs): "))
    fresh_wingspan, fresh_vertical = find_fresh_measurable(
        fresh_height, curr_height)

  pred_height = height_pred(fresh_height)
  pred_weight = weight_pred(fresh_weight)
  pred_wingspan = wingspan_pred(fresh_wingspan)
  pred_vertical = vertical_pred(fresh_vertical)
  print()
  print("Predicted Measurables:")

  print(f"Height: {pred_height}")
  print(f"Weight: {pred_weight}")
  print(f"Wingspan: {pred_wingspan}")
  print(f"Vertical: {pred_vertical}")


'''
while(True):
  input("Player Name: ")
  print()
  measurable_pred_asker()
  print()
'''
#print(vertical_pred(27))
#print(vertical_pred_nonFresh(74.5,74.5,27))