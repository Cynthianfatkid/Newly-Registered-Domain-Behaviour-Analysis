import random
from datetime import date
from datetime import timedelta

today = date.today()

# Yesterday date
yesterday = today - timedelta(days = 1)

def pick_random_domains(filename, num_domains):
    """Picks num_domains unique domain names randomly from a text file.

    Args:
        filename (str): The path to the text file containing the domain names.
        num_domains (int): The number of random domain names to pick.

    Returns:
        list: A list of the randomly selected domain names.
    """

    with open("YOUR_PATH" + str(yesterday) + "/domain-names.txt", 'r') as file:
        domains = file.read().splitlines()  # Read lines into a list

    random.shuffle(domains)  # Shuffle the list in-place
    random_domains = domains[:num_domains]  # Take the first 500 unique domains

    return random_domains

# Example usage:
filename = "random_domains_"+ str(yesterday) + ".txt"  # Replace with your actual filename
random_domains = pick_random_domains(filename, 1000)

# Save
with open("YOUR_PATH"+filename, "w") as file:
  #for line in unique_random_lines:
  file.write("\n".join(random_domains))
