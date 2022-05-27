from redis_lookup import lookup_forex


def convert(From="USD", To="NPR", value=1):
    forex_rate = lookup_forex(From, To)

    if forex_rate == -1:
        return "invalid currency or the currency is not yet\
                availabe in the database"

    return forex_rate * value


if __name__ == "__main__":
    # print(convert(To="USD", From="NPR", value=200))
    print(convert())
