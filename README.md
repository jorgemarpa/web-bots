# Web-bots

This is a collection of python scripts to do web scraping.

- `check_cl.py` and `check_pb.py` checks for bike ads in Craigslist and PinkBike.
I can provide the bike brand and model using the keyword arguments
`--brand` and `--model`. Here's an example:

```python
❯ python check_cl.py --brand transition --model spur

I found the following ads:
Result (1)
	Ad   :  2021 Transition Spur Custom 26.73 lbs Reserve Wheels X01 XL
	Price:  $6,250
	Dist :  65.3mi
	Loc  :  (sfo > concord / pleasant hill / martinez)
	Link :  https://sfbay.craigslist.org/eby/bik/d/pleasant-hill-2021-transition-spur/7458360780.html
```
