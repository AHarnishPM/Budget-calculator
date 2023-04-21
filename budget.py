class Category:
  pct_total = 0
  
  def __init__(self, group):
    self.group = group
    self.ledger = []

  def __str__(self):
    stars = "*"*(15 - len(self.group)//2)
    head = stars + self.group + stars + "\n"
    
    
    transactions = ""
    for i in self.ledger:
      i["amount"] = "{:.2f}".format(i["amount"])
      cropped_description = i["description"][:23]
      gap = " "*(30 - len(str(i["amount"])) - len(cropped_description))
      transactions += cropped_description + gap + str(i["amount"]) + "\n"
      total = "Total: " + str(self.get_balance())

    
    return head + transactions + total

  def deposit(self, amount, description=""):
    self.amount = amount
    self.description = description
    self.ledger.append({"amount":self.amount, "description":self.description})

  def withdraw(self, amount, description=""):
    self.amount = -1*amount
    self.description = description
    
    if self.check_funds(amount):
      self.ledger.append({"amount":self.amount, "description":self.description})
      return True
    else:
      return False

  def get_balance(self):
    balance = 0
    for i in self.ledger:
      balance += float(i['amount'])
    return balance
      
  def transfer(self, amount, other_category):
    self.amount = amount
    if self.check_funds(self.amount):
      self.withdraw(self.amount, "Transfer to " + other_category.group)
      self.amount *= -1
      other_category.deposit(self.amount, "Transfer from " + self.group)

      return True
    else:
      return False


  def check_funds(self, amount):

    balance = 0
    for i in self.ledger:
      balance += i['amount']
    if amount > balance:
      return False
    else:
      return True

  def total_spending(self):
    group_total_spending = 0
    for i in self.ledger:
      if float(i["amount"]) < 0:
        group_total_spending += float(i["amount"])
    return group_total_spending
    

def create_spend_chart(categories):

  graph = ""

  graph += "Percentage spent by category\n"
  
  total = 0
  
  for i in categories:
    total += i.total_spending()

  for i in categories:
    i.pct_total += (i.total_spending()/total)//.10

  for i in reversed(range(11)):
    prnt = ""
    prnt += " "*(3-len(str(i*10))) + str(int(10*i)) + "|"
    for j in categories:
      if j.pct_total >= i:
        prnt += " o "
      else:
        prnt += "   "
    graph += prnt + " \n"

  ccount = 0
  for i in categories:
    ccount += 3
  graph += ("    -" + "-"*ccount + "\n")

  empty = 0
  count = 0

  while empty < len(categories) and count < 100:
    empty = 0
    line = "    "
    for i in categories:
      try:
        line += " " + i.group[count] + " "
      except IndexError:
        line += "   "
        empty += 1
    count += 1

    if empty < len(categories):
      graph += line + " \n"

  return graph[:-1]

    
  
  
    