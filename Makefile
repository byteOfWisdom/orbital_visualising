all:
	python3 render.py data/osc_$(m)_0.dat "1S0 -> 2P$(m), wt=0.0" $(m)
	python3 render.py data/osc_$(m)_1.dat "1S0 -> 2P$(m), wt=1.0" $(m)
	python3 render.py data/osc_$(m)_2.dat "1S0 -> 2P$(m), wt=2.0" $(m)
	python3 render.py data/osc_$(m)_3.dat "1S0 -> 2P$(m), wt=3.0" $(m)
	python3 render.py data/osc_$(m)_4.dat "1S0 -> 2P$(m), wt=4.0" $(m)
	python3 render.py data/osc_$(m)_5.dat "1S0 -> 2P$(m), wt=5.0" $(m)
	python3 render.py data/osc_$(m)_6.dat "1S0 -> 2P$(m), wt=6.0" $(m)

render_states:
	python3 render.py data/1s0.dat "1S0" 0
	python3 render.py data/2p0.dat "2P0" 0
	python3 render.py data/2p-1.dat "2P-1" 1
	python3 render.py data/2p1.dat "2P1" 1

gen:
	go run gen.go $(m) 0.0 > data/osc_$(m)_0.dat
	go run gen.go $(m) 1.0 > data/osc_$(m)_1.dat
	go run gen.go $(m) 2.0 > data/osc_$(m)_2.dat
	go run gen.go $(m) 3.0 > data/osc_$(m)_3.dat
	go run gen.go $(m) 4.0 > data/osc_$(m)_4.dat
	go run gen.go $(m) 5.0 > data/osc_$(m)_5.dat
	go run gen.go $(m) 6.0 > data/osc_$(m)_6.dat

gen_states:
	go run gen.go s 1 0 0 > data/1s0.dat
	go run gen.go s 2 1 0 > data/2p0.dat
	go run gen.go s 2 1 -1 > data/2p1.dat
	go run gen.go s 2 1 1 > data/2p-1.dat
