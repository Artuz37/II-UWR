use ggez::*;

pub struct Berry {
    pub position: na::Point2<f32>,
}

impl Berry {
    pub fn new(rng: &mut ThreadRng) -> Berry {
        let x_pos : f32 = rng.gen_range(0.0, 780.0);
        let y_pos : f32 = rng.gen_range(0.0, 560.0);

        Berry {
            position: na::Point2::new(x_pos, y_pos),
        }
    }
}