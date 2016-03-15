#include "colors.inc"
#include "textures.inc"


camera {
	location 1.08*<3,4,-6>
	look_at 0
}

light_source{
	<7,20,-15>
	White
	spotlight
	point_at <0,0,2>
	radius 16
	falloff 30
}

light_source{
	<-7,20,-15>
	White
	spotlight
	point_at <0,0,2>
	radius 16
	falloff 30
}

light_source{<5,0,0> 0.5*White shadowless}
light_source{<0,0,-5> 0.4*White shadowless}
light_source{<-5,0,0> 0.5*White shadowless}
light_source{<0,0,5> 0.4*White shadowless}


#macro CMirror(p, d, r, s)
	intersection{
		difference {sphere{p+r*vnormalize(d), r} sphere{p+r*vnormalize(d), 0.98*r}}
		cylinder {p-0.01*vnormalize(d), p+r*vnormalize(d), s}
	}
#end

#declare Orange = rgb<1,0.3,0>;

object {
	CMirror(<-3,1,3>, <-3,1,3>, 7.5, 2)
	texture{
	pigment{color Black}
		finish{reflection 1 diffuse 0 specular 0.3 }
	}
}

plane{
	y, -3
	texture{
		pigment{color 0.7*White}
		finish{reflection 0.9 diffuse 0.2 ambient 0.05}
	}
}


#declare margin = 0.08;
#declare th = 0.001;

#macro Sticker(d, o1, o2, col)
	box {
		(0.5-th)*d - (0.5-margin)*o1 - (0.5-margin)*o2
		(0.5+th)*d + (0.5-margin)*o1 + (0.5-margin)*o2
		texture{
			pigment{color col}
		}
	}
#end


#declare Blank = rgbft<0,0,0,0,1>;


#macro Cubie(F, R, U, B, L, D, tr) //Cubie with edge length 1, centred at origin, with face colours as indicated. Use Blank to simulate no sticker
	union{
		superellipsoid {
			<0.12, 0.12>
			scale 0.5
			texture{
				pigment{color 0.05*White}
				finish{specular 0.3}
			}
		}
		Sticker(-z, x, y, F)
		Sticker(+z, x, y, B) //+z is the same as z, + only for emphasis
		Sticker(+x, y, z, R)
		Sticker(-x, y, z, L)
		Sticker(+y, z, x, U)
		Sticker(-y, z, x, D)
		scale 0.999
		translate tr
	}
#end

#declare rot = (1-cos(pi*clock))/2;