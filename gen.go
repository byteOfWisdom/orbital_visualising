package main

import (
	"fmt"
	"math"
	"math/cmplx"
	"os"
	"strconv"
)

func binomial(n int, k int) float64 {
	return factorial(n) / (factorial(k) * factorial(n-k))
}

func factorial(x int) float64 {
	res := 1.0
	for i := 1; i <= x; i += 1 {
		res *= float64(i)
	}
	return res
}

func laguerre(s int, t int, x float64) float64 {
	var res = 0.0

	for i := 0; i < t-s+1; i += 1 {
		sign := math.Pow(-1.0, float64(i))
		res += sign * binomial(s, t) * math.Pow(x, float64(t)) / factorial(t)
	}

	return res
}

func radial(r float64, n, l int) complex128 {
	a := -math.Sqrt(factorial(n-l-1) / (float64(2*n) * math.Pow(factorial(n+l), 3)))
	b := math.Pow(2.0/float64(n), 3.0/2.0)
	c := math.Pow(2.0*r/float64(n), float64(l))
	d := math.Exp(-r / float64(n))
	return complex(a*b*c*d*laguerre((2*l)+1, (n+l), 2.0*r/float64(n)), 0)
}

func angular(theta, phi float64, l, m int) complex128 {
	if l == 0 {
		return complex(math.Sqrt(1.0/(4*math.Pi)), 0.0)
	}
	if l == 1 {
		if m == -1 {
			return complex(math.Sqrt(3.0/(8.0*math.Pi))*math.Sin(theta), 0.0) * cmplx.Exp(complex(0.0, -phi))
		}
		if m == 0 {
			return complex(math.Sqrt(3.0/(4.0*math.Pi))*math.Cos(theta), 0.0)
		}
		if m == 1 {
			return complex(-math.Sqrt(3.0/(8.0*math.Pi))*math.Sin(theta), 0.0) * cmplx.Exp(complex(0.0, phi))
		}
	}
	return complex(0, 0)
}

func sgl(r, theta, phi float64, n, l, m int) complex128 {
	return radial(r, n, l) * angular(theta, phi, l, m)
}

func spherical(x, y, z float64) (float64, float64, float64) {
	r := math.Sqrt(x*x + y*y + z*z)
	theta := math.Acos(z / r)
	phi := math.Atan(y / x)
	return r, theta, phi
}

func superpos(r, theta, phi float64, n1, l1, m1, n2, l2, m2 int, phase float64) complex128 {
	w1 := sgl(r, theta, phi, n1, l1, m1)
	w2 := sgl(r, theta, phi, n2, l2, m2)
	norm := complex(1.0/math.Sqrt(2.0), 0.0)
	return norm * (w1 + complex(0, 1)*cmplx.Exp(complex(0, -phase))*w2)
}

func cal_superpos(lim, h float64, m int, phase float64) {
	for x := -lim; x <= lim; x += h {
		for y := -lim; y <= lim; y += h {
			for z := -lim; z <= lim; z += h {
				r, theta, phi := spherical(x, y, z)
				wave := superpos(r, theta, phi, 1, 0, 0, 2, 1, m, phase)
				value := math.Pow(cmplx.Abs(wave), 2.0)
				fmt.Printf("%f %f %f %.15f\n", x, y, z, value)
			}
		}
	}
}

func cal_single_state(lim, h float64, n, l, m int) {
	for x := -lim; x <= lim; x += h {
		for y := -lim; y <= lim; y += h {
			for z := -lim; z <= lim; z += h {
				r, theta, phi := spherical(x, y, z)
				wave := sgl(r, theta, phi, n, l, m)
				value := math.Pow(cmplx.Abs(wave), 2.0)
				fmt.Printf("%f %f %f %.15f\n", x, y, z, value)
			}
		}
	}
}

func main() {
	lim := 15.0
	h := 0.5
	if os.Args[1] == "s" {
		n, _ := strconv.Atoi(os.Args[2])
		l, _ := strconv.Atoi(os.Args[3])
		m, _ := strconv.Atoi(os.Args[4])

		cal_single_state(lim, h, n, l, m)
	} else {
		m, _ := strconv.Atoi(os.Args[1])
		phase, _ := strconv.ParseFloat(os.Args[2], 64)
		cal_superpos(lim, h, m, phase)
	}

}
