use nalgebra as na;
use rand::rngs::ThreadRng;
use rand::{self, Rng};

use ggez::*;

const HEALTH: f32 = 2000.0;

fn mutation() -> f32{
    let mut rng = rand::thread_rng();
    let mut mutation = rng.gen_range(0.8, 1.2);
    if rng.gen::<bool>(){mutation = 1.0;}
    mutation
}

fn sign() -> f32 {
    let num = rand::thread_rng().gen_range(0, 100);
    if num < 50{return -1.0;}    
    else {return 1.0};
}

fn dist(p1: na::Point2<f32>, p2: na::Point2<f32>) -> f32{
    ((p1.x - p2.x).powi(2) + (p1.y - p2.y).powi(2)).sqrt()
}


#[derive(Copy, Clone)]
pub struct Bunny {
    pub position: na::Point2<f32>,
    pub velocity: na::Vector2<f32>,
    pub speed: f32,
    pub hunger: f32,
    pub radius: f32,
    pub libido: f32,
    pub male: bool,
    pub reproduced: f32,
    pub health: f32,
}

impl Bunny {
    pub fn new(rng: &mut ThreadRng, sex: bool) -> Bunny {
        let speed = rng.gen_range(0.5, 2.0);
        let x_vel : f32 = rng.gen_range(-speed, speed);
        let y_vel : f32 = sign()*((speed*speed - x_vel*x_vel).abs().sqrt());
        let x_pos : f32 = rng.gen_range(0.0, 780.0);
        let y_pos : f32 = rng.gen_range(0.0, 560.0);
        let lib : f32 = rng.gen_range(10.0, 90.0);
        let rad = rng.gen_range(100.0, 400.0);


        Bunny {
            position: na::Point2::new(x_pos, y_pos),
            velocity: na::Vector2::new(x_vel, y_vel),
            speed: speed,
            hunger: 0.0,
            radius: 300.0,
            libido: lib,
            male: sex,
            reproduced: 0.0,
            health: HEALTH,
        }
    }

    pub fn direction(&mut self, place: na::Point2<f32>) -> na::Vector2<f32> {
        let ratio = dist(self.position, place)/self.speed;
        let x_vel = (place.x - self.position.x)/ratio;
        let y_vel = (place.y - self.position.y)/ratio;
        na::Vector2::new(x_vel, y_vel)
    }

    pub fn sense(&mut self, berry: &mut Berry) -> bool{
        let distance = dist(self.position, berry.position);
        distance < self.radius
    }

    pub fn mating(&mut self, mate: &Bunny) -> bool {
        //if mate.libido < mate.hunger && mate.reproduced > 0.0{return false}
        //if mate.male{return false}
        let distance = dist(self.position, mate.position);
        distance < self.radius && mate.libido > mate.hunger && mate.reproduced <= 0.0
    }

    pub fn can_mate(&mut self, mate: &Bunny) -> bool {
        (self.position.x - mate.position.x).abs() < 26.0 && (self.position.y - mate.position.y).abs() < 37.0 && mate.reproduced <= 0.0 && mate.hunger < mate.libido
    }

    pub fn reproduce(&mut self, mom: &mut Bunny) -> Bunny{
        let mut rng = rand::thread_rng();
        let x_pos = mom.position.x + 0.3;
        let y_pos = mom.position.y + 0.3;
        let mut speed = self.speed*mutation();
        if rng.gen::<bool>() {speed = mom.speed*mutation();}
        let mut libido = self.libido*mutation();
        if rng.gen::<bool>(){libido = mom.libido*mutation();}
        let mut radius = self.radius*mutation();
        if rng.gen::<bool>(){radius = mom.radius*mutation();}

        let x_vel : f32 = rng.gen_range(-speed, speed);
        let y_vel : f32 = sign()*((speed*speed - x_vel*x_vel).abs().sqrt());
        
        Bunny {
            position: na::Point2::new(x_pos, y_pos),
            velocity: na::Vector2::new(x_vel, y_vel),
            speed: speed,
            hunger: libido,
            radius: radius,
            libido: libido,
            male: rng.gen::<bool>(),
            reproduced: 200.0,
            health: HEALTH,
        }
    }

    pub fn eats(&mut self, berry: &mut Berry) -> bool{
        let bun_x = self.position.x;
        let bun_y = self.position.y;
        let ber_x = berry.position.x;
        let ber_y = berry.position.y;
        if (bun_x - ber_x).abs() < 26.0 && -29.0 < bun_y - ber_y && bun_y - ber_y < 37.0{
            self.hunger = 0.0;
            return true;
        } 
        false
    }

    pub fn redirect(&mut self, rng: &mut ThreadRng) {
        let x_vel : f32 = rng.gen_range(-self.speed, self.speed);
        let y_vel : f32 = sign()*((self.speed*self.speed - x_vel*x_vel).abs().sqrt());
        self.velocity = na::Vector2::new(x_vel, y_vel);
    }
    pub fn Copy(self) -> Bunny{
        let vel = self.velocity;
        let pos = self.position;
        let spd = self.speed;
        let hunger = self.hunger;
        let radius = self.radius;

        Bunny {
            position: pos,
            velocity: vel,
            speed: spd,
            hunger: hunger,
            radius: radius,
            libido: self.libido,
            male: self.male,
            reproduced: self.reproduced,
            health: self.health,
        }
    }
}

pub struct Berry {
    pub position: na::Point2<f32>,
}

impl Berry {
    pub fn new(rng: &mut ThreadRng) -> Berry {
        let x_pos : f32 = rng.gen_range(0.0, 780.0);
        let y_pos : f32 = rng.gen_range(0.0, 460.0);

        Berry {
            position: na::Point2::new(x_pos, y_pos),
        }
    }
}