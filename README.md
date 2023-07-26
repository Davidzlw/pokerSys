# Base Class



### class Suit(Enum):

##### methods:

```
short() -> the symbol for suit
```



### class Point(IntEnum):



### class Card:

##### elements:

| element | Type  |
| ------- | ----- |
| suit    | Suit  |
| point   | Point |

##### methods:

```
__str__() -> can print directly
```



### calss Categories:

base class for hand value



### class HighCard(Categories)

##### elements:

| element  | Type   | Value       |
| -------- | ------ | ----------- |
| cat_name | string | "HighCard"  |
| rank     | int    | 1           |
| points   | [int]  | [x,x,x,x,x] |



##### methods:

```
info(): -> description of this category
```



### class Pair(Categories)

##### elements:

| element  | Type   | Value   |
| -------- | ------ | ------- |
| cat_name | string | "Pair"  |
| rank     | int    | 2       |
| pair     | int    | pair    |
| kickers  | [int]  | kickers |



##### methods:

```
info(): -> description of this category
```



### class TwoPair(Categories)

##### elements:

| element  | Type   | Value     |
| -------- | ------ | --------- |
| cat_name | string | "TwoPair" |
| rank     | int    | 3         |
| tpair    | int    | tpair     |
| npair    | int    | npair     |
| kicker   | int    | kicker    |



##### methods:

```
info(): -> description of this category
```



### class Set(Categories)

##### elements:

| element  | Type   | Value   |
| -------- | ------ | ------- |
| cat_name | string | "Set"   |
| rank     | int    | 4       |
| set      | int    | set     |
| kickers  | [int]  | kickers |



##### methods:

```
info(): -> description of this category
```



### class Straight(Categories)

##### elements:

| element  | Type   | Value      |
| -------- | ------ | ---------- |
| cat_name | string | "Straight" |
| rank     | int    | 5          |
| high     | int    | high       |



##### methods:

```
info(): -> description of this category
```



### class Flush(Categories)

##### elements:

| element  | Type   | Value   |
| -------- | ------ | ------- |
| cat_name | string | "Flush" |
| rank     | int    | 6       |
| suit     | Suit   | suit    |
| points   | [int]  | points  |



##### methods:

```
info(): -> description of this category
```



### class FullHouse(Categories)

##### elements:

| element  | Type   | Value       |
| -------- | ------ | ----------- |
| cat_name | string | "FullHouse" |
| rank     | int    | 7           |
| set      | int    | set         |
| pair     | int    | pair        |



##### methods:

```
info(): -> description of this category
```



### class Quart(Categories)

##### elements:

| element  | Type   | Value   |
| -------- | ------ | ------- |
| cat_name | string | "Quart" |
| rank     | int    | 8       |
| quart    | int    | quart   |
| kicker   | int    | kicker  |



##### methods:

```
info(): -> description of this category
```



### class StraightFlush(Categories)

##### elements:

| element  | Type   | Value           |
| -------- | ------ | --------------- |
| cat_name | string | "StraightFlush" |
| rank     | int    | 9               |
| suit     | Suit   | suit            |
| high     | int    | high            |



##### methods:

```
info(): -> description of this category
```



### class Result

##### elements:

| element   | Type       | Value     |
| --------- | ---------- | --------- |
| player_id | int        | player_id |
| cat       | Categories | cat       |





# Judger



### class Judge

##### elements:

| element | Type  | Value                        |
| ------- | ----- | ---------------------------- |
| board   | [int] | [x,x,x,x,x], community cards |



##### methods:

```
count_suit(combine: [Card])  -> return a map cnt, cnt[suit] means number of suit in combine (7 cards)
```



```
count_point(combine: [Card])  -> return a map cnt, cnt[point] means number of point in combine (7 cards)
```



```
highest_straight(combine: [Card])  -> return a int highest, means the lowest point of the highest straight occurs in combine (7 cards)
```

highest_straight([2 3 4 5 6 7]) is 3



```
rank(combine: [Card])  -> return the specific Category of given combine(7 cards)
```



```
pk(results: [Result]):  -> return a list of results that wins
```



```
judge(board: [Card], players: []):  -> return play id of winners
```

>  rank()  to get the hand value of each player.
>
>  pk() to get winners 



# Player

### class Player

##### elements:

| element | Type         | Value     |
| ------- | ------------ | --------- |
| id      | int          | player_id |
| name    | string       | name      |
| hand    | [Card, Card] | hand      |





# Dealer

### class Dealer

##### elements:

| element | Type   | Value                  |
| ------- | ------ | ---------------------- |
| game    | System | callback of game sys   |
| piles   | [Card] | pile cards             |
| board   | [Card] | board, community cards |



##### methods:

```
shuffle()  -> shuffle all 52 pile cards and return [cards]
```



```
choose_5()  -> random draw 5 cards and return [cards]
```



```
draw()  -> draw the top of the pile and return
```



```
draw_spec()  -> draw a specific card of the pile and return
```



```
deliver_to_player(i)  -> call draw() twice to deliver a hand to ith player
```



```
deliver_to_all()  -> deliver every player's hand
```



------

```
flop()  -> board [] => [x, x, x]
turn()  -> board [x, x, x] => [x, x, x, x]
river() -> board [x, x, x, x] => [x, x, x, x, x]
```



```
show_hands()  -> print every player's hand
```



```
show_board()  -> print board's card
```



# System



### class System

##### elements:

| element   | Type       | Value                                |
| --------- | ---------- | ------------------------------------ |
| dealer    | Dealer     |                                      |
| judger    | Judge      |                                      |
| rounds    | []         | ["preflop", "flop", "turn", "river"] |
| round_id  | int        | 0                                    |
| nplayer   | int        | n                                    |
| players   | [Player]   |                                      |
| manager   | PotManager |                                      |
| button_id | 0          |                                      |



##### methods:

```
run()  -> start a whole game
```

> progerss:
>
> ```python
> dealer.shuffle()
> dealer.deliver_to_all()
> manager.every_game_init()
> manager.round()
> dealer.flop()
> manager.round()
> dealer.turn()
> manager.round()
> dealer.river()
> manager.round()
> dealer.show_hands()
> dealer.show_board()
> judge.judge(dealer.board, players)
> ```

