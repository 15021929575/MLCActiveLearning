CXXFLAGS = -Wall -O3
LDFLAGS = -lm
sample.out: sample.o spatial.o
	$(CXX) -o $@ $+ $(LDFLAGS)
clean:
	rm -f *.o sample.out
