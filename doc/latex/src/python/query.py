def __query(self, your_query):
        """
        Make your own query in the specified table. Make sure to only give a SELECT statement, otherwise your query won't work.
        """
        self.__cursor.execute(your_query)
        return self.__cursor.fetchall()