# print([*range(1, 52, 13)])

list_of_cards = ["A", "2", "3", "4", "5", "6", \
                 "7", "8", "9", "10", "J", "Q", "K"]

# for i in range(0,13):
#     print(f"{list_of_cards[i]}:")
#     print([*range(i+1, 53, 13)])

# print([*range(1,53)])
print("Hearts:", [*range(1, 14)])
print("Diamonds:", [*range(14, 28)])
print("Clubs:", [*range(28, 40)])
print("Spades:", [*range(40, 53)], '\n')
print(56//13)
# for i in range(2600,2700):
#     print(i, chr(i))

print('\033[1m' + 'Hello' + '\033[0m')
print('\033[4m' + 'Hello' + '\033[0m')

print('\033[1m' + '\033[47m' + '\033[31m' + ' Hello ' + '\033[0m')

a = [5, 2, 3, 6, 4]
# is_straight = all(a[i] == a[i-1] + 1 for i in range(1, len(a)))
is_straight = (max(a) - min(a) + 1) == len(a)
print(is_straight)
a.sort()
print(a)
print('\033[1;38;2;255;255;255;7;41m' + u' \u2665 A ' + '\033[0m')
print('\033[1;38;2;255;255;255;7m' + u' \u2660 A ' + '\033[0m')
print('\033[1;38;2;255;255;255;7;41m' + u' \u2666 A ' + '\033[0m')
print('\033[1;38;2;255;255;255;7m' + u' \u2663 A ' + '\033[0m')

print("")

for i in list_of_cards:
    print(f'\033[1;38;2;255;255;255;7;41m' + f' \u2665 {i} ' + '\033[0m' + \
            '\t' + f'\033[1;38;2;255;255;255;7m' + f' \u2660 {i} ' + '\033[0m' + \
            '\t' + f'\033[1;38;2;255;255;255;7;41m' + f' \u2666 {i} ' + '\033[0m' + \
            '\t' + f'\033[1;38;2;255;255;255;7m' + f' \u2663 {i} ' + '\033[0m')


print(u'\u2665\u2660\u2666\u2663')