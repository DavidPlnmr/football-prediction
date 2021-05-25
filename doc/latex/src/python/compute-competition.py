def compute_competition(self):
    """
    Compute the whole competitions using multiprocessing
    """
    if len(self.history) <= 0:
        matches = []
        for first_team in self.standings:
            for second_team in self.standings:
                exist = False
                
                if [first_team["Name"],second_team["Name"]] in matches or [second_team["Name"],first_team["Name"]] in matches:
                    exist = True
                    
                if first_team["Name"] != second_team["Name"] and not exist:    
                    matches.append([
                        first_team["Name"],
                        second_team["Name"]
                    ])
                pass
            pass
        
        #start = time.perf_counter()
        
        threads = len(matches)   # Number of threads to create
        manager = multiprocessing.Manager()
        out_list = manager.list()
        
        # Create a list of jobs and then iterate through
        # the number of threads appending each thread to
        # the job list 
        jobs = []
        
        for i in range(0, threads):
            thread = multiprocessing.Process(target=self.make_prediction, 
                                        args=(matches[i][0], matches[i][1], out_list))
            jobs.append(thread)

        # Start the threads 
        for j in jobs:
            j.start()
            time.sleep(0.1)

        # Ensure all of the threads have finished
        for j in jobs:
            
            j.join()    
        
        #end = time.perf_counter()
        #print(f"Finished in {end-start} seconds")
        print(len(out_list))
        print(threads)
        self.history = out_list
    return self.history