mod bunny;
use bunny::Bunny;
use bunny::Berry;
use std::env;
use std::path;

use std::collections::HashSet;

use nalgebra as na;
use rand::rngs::ThreadRng;
use rand::{self, Rng};

use ggez::graphics::{spritebatch::SpriteBatch, Color, Image};
use ggez::Context;
use ggez::*;

// NOTE: Using a high number here yields worse performance than adding more bunnies over
// time - I think this is due to all of the RNG being run on the same tick...
const INITIAL_BUNNIES: usize = 10;
const INITIAL_BERRIES: usize = 10;
const WIDTH: u16 = 800;
const HEIGHT: u16 = 600;
const FOOD_TIMER: i32 = 100;
const SCORE_BOX_FIELD: graphics::Rect = graphics::Rect::new(0.0, 520.0, 800.0, 81.0);
const SCORE_BOX_COLOR: graphics::Color = graphics::Color::new(56.0/255.0, 66.0/255.0, 59.0/255.0, 1.0);

const BOTTOM_LINE_CORDS: &[mint::Point2<f32>] = &[(mint::Point2 {x: 0.0, y: 520.0}), (mint::Point2 {x: 800.0, y: 520.0})];


fn dist(p1: na::Point2<f32>, p2: na::Point2<f32>) -> f32{
    ((p1.x - p2.x).powi(2) + (p1.y - p2.y).powi(2)).sqrt()
}


struct GameState {
    rng: ThreadRng,
    texture: Image,
    girl_texture: Image,
    berry_texture: Image,
    bunnies: Vec<Bunny>,
    hoes: Vec<Bunny>,
    berries: Vec<Berry>,
    max_x: f32,
    max_y: f32,
    means: Vec<f32>,
    background: Image,
    bottomline: graphics::Mesh,

    click_timer: i32,
    bunnybatch: SpriteBatch,
    berrybatch: SpriteBatch,
    batched_drawing: bool,
}

impl GameState {
    fn new(ctx: &mut Context) -> ggez::GameResult<GameState> {
        let mut rng = rand::thread_rng();
        let texture = Image::new(ctx, "/wabbit_alpha.png")?;
        let girl_texture = Image::new(ctx, "/wabbit_beta.png")?;
        let berry_texture = Image::new(ctx, "/smallberry.png")?;
        let background = Image::new(ctx, "/grass.jpg")?;
        let mut bunnies = Vec::with_capacity(INITIAL_BUNNIES);
        let mut hoes = Vec::with_capacity(INITIAL_BUNNIES);
        let mut berries = Vec::new();
        let max_x = (WIDTH - texture.width()) as f32;
        let max_y = (HEIGHT - 80 - texture.height()) as f32;

        for _ in 0..INITIAL_BUNNIES { 
            bunnies.push(Bunny::new(&mut rng, true));
        }
        for _ in 0..INITIAL_BUNNIES { 
            hoes.push(Bunny::new(&mut rng, false));
        }
        for _ in 0..INITIAL_BERRIES {
            berries.push(Berry::new(&mut rng));
        }
        let berrybatch = SpriteBatch::new(berry_texture.clone());
        let bunnybatch = SpriteBatch::new(texture.clone());
        
        let mut means : Vec<f32> = vec![0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
        for bunny in &bunnies{
            means[0] += bunny.speed;
            means[1] += bunny.libido;
            means[2] += bunny.radius;
        }
        for bunny in &hoes{
            means[3] += bunny.speed;
            means[4] += bunny.libido;
            means[5] += bunny.radius;
        }
        means = means.into_iter().map(|x| x/INITIAL_BUNNIES as f32).collect();

        let bottomline: graphics::Mesh = graphics::Mesh::new_line(ctx, BOTTOM_LINE_CORDS, 5.0, [0.0, 0.0, 0.0, 1.0].into())
            .expect("main.rs/GameState/draw(): Couldn't create bottom_line");

        Ok(GameState {
            rng,
            texture,
            girl_texture,
            berry_texture,
            bunnies,
            hoes,
            berries,
            max_x,
            max_y,
            means,
            background,
            bottomline,

            click_timer: 0,
            bunnybatch,
            berrybatch,
            batched_drawing: false,
        })
    }
}

impl event::EventHandler for GameState {
    fn update(&mut self, _ctx: &mut Context) -> GameResult {
        self.click_timer -= 1;
        if self.click_timer < 0 && self.bunnies.len() < 100 {
            self.berries.push(Berry::new(&mut self.rng));
            self.berries.push(Berry::new(&mut self.rng));
            self.click_timer = FOOD_TIMER;
        }
        let mut eliminate: Vec<na::Point2<f32>> = vec![];
        let mut kids: Vec<Bunny> = vec![];
        let mut tracing: bool = false;
        for bunny in &mut self.bunnies {
            if bunny.reproduced > 0.0 {bunny.reproduced -= 0.5;}
            bunny.health -= 1.0;
            bunny.hunger += bunny.speed*0.1;
            if bunny.hunger > 100.0 || bunny.health < 0.0 {
                eliminate.push(bunny.position);
                continue;
            }

            bunny.position += bunny.velocity;
            if bunny.position.x > self.max_x {
                bunny.velocity.x *= -1.0;
                bunny.position.x = self.max_x;
            } else if bunny.position.x < 0.0 {
                bunny.velocity.x *= -1.0;
                bunny.position.x = 0.0;
            }

            if bunny.position.y > self.max_y {
                bunny.velocity.y *= -1.0;
                bunny.position.y = self.max_y;
                //self.rng.gen::<bool>()
            } else if bunny.position.y < 0.0 {
                bunny.velocity.y *= -1.0;
                bunny.position.y = 0.0;
            }

            //food chasin'
            let mut eat: Vec<na::Point2<f32>> = vec![];
            let mut closest_smth = 1000.0;
            let mut vec = bunny.velocity;
            if bunny.hunger > bunny.libido && bunny.reproduced > 0.0 {
                for berry in &mut self.berries {
                    if bunny.eats(berry){
                        eat.push(berry.position);
                        tracing = false;
                        break;
                    }
                    if bunny.sense(berry){
                        if dist(bunny.position, berry.position) < closest_smth{
                            closest_smth = dist(bunny.position, berry.position);
                            vec = bunny.direction(berry.position);
                        }
                        tracing = true;
                    }
                }
                for ber in eat{  //girls food
                    let index = self.berries.iter().position(|x| *x.position == *ber).unwrap();
                    self.berries.remove(index);
                }
            } 

            else if bunny.reproduced <= 0.0 {
                for mate in &mut self.hoes{  //matin' mechanic
                    if bunny.can_mate(mate) {
                        mate.reproduced = 100.0;
                        bunny.reproduced = 100.0;
                        kids.push(bunny.reproduce(mate));
                        tracing = false;
                        break;
                    };
                    if bunny.mating(mate){
                        if dist(bunny.position, mate.position) < closest_smth{
                            closest_smth = dist(bunny.position, mate.position);
                            vec = bunny.direction(mate.position);
                        }
                        tracing = true;
                    }
                }
            }

            bunny.velocity = vec;
            if !tracing && self.rng.gen_range(0, 100) == 7 {
                bunny.redirect(&mut self.rng);
            }
        }

        for bun in eliminate{  // killin' boys
            let index = self.bunnies.iter().position(|x| *x.position == *bun).unwrap();
            self.bunnies.remove(index);
        }
        
        let mut eliminate: Vec<na::Point2<f32>> = vec![];

        for bunny in &mut self.hoes {
            if bunny.reproduced > 0.0 {bunny.reproduced -= 0.5;}
            bunny.health -= 1.0;
            bunny.hunger += bunny.speed*0.1;
            if bunny.hunger > 100.0 || bunny.health < 0.0 {
                eliminate.push(bunny.position);
                continue;
            }

            bunny.position += bunny.velocity;
            if bunny.position.x > self.max_x {
                bunny.velocity.x *= -1.0;
                bunny.position.x = self.max_x;
            } else if bunny.position.x < 0.0 {
                bunny.velocity.x *= -1.0;
                bunny.position.x = 0.0;
            }

            if bunny.position.y > self.max_y {
                bunny.velocity.y *= -1.0;
                bunny.position.y = self.max_y;
                //self.rng.gen::<bool>()
            } else if bunny.position.y < 0.0 {
                bunny.velocity.y *= -1.0;
                bunny.position.y = 0.0;
            }

            //food chasin'
            let mut closest_smth = 1000.0;
            let mut vec = bunny.velocity;
            let mut eat: Vec<na::Point2<f32>> = vec![];
            if bunny.hunger > bunny.libido   {for berry in &mut self.berries {
                    if bunny.eats(berry){
                        eat.push(berry.position);
                        tracing = false;
                        break;
                    }
                    if bunny.sense(berry){
                        if dist(bunny.position, berry.position) < closest_smth{
                            closest_smth = dist(bunny.position, berry.position);
                            vec = bunny.direction(berry.position);
                        }
                        tracing = true;
                    }
                }}
            for ber in eat{  //girls food
                let index = self.berries.iter().position(|x| *x.position == *ber).unwrap();
                self.berries.remove(index);
            }

            bunny.velocity = vec;
            if !tracing && self.rng.gen_range(0, 100) == 7 {
                bunny.redirect(&mut self.rng);
            }
        }
        
        for bun in eliminate{    //killin' girls
            let index = self.hoes.iter().position(|x| *x.position == *bun).unwrap();
            self.hoes.remove(index);
        }

        for bby in kids{
            if bby.male{self.bunnies.push(bby);}
            else {self.hoes.push(bby);}
        }
        // let bunn = &self.bunnies;
        // self.bunnies = bunn.into_iter().filter(|x| eliminate.contains(&x.position)).collect();
        //self.bunnies = new_bunnies;
        
        Ok(())
    }

    fn draw(&mut self, ctx: &mut Context) -> GameResult {
        graphics::clear(ctx, Color::from((0.392, 0.584, 0.929)));
        graphics::draw(ctx, &self.background, graphics::DrawParam::default())?;
        if self.batched_drawing {
            self.bunnybatch.clear();
            self.berrybatch.clear();
            for bunny in &self.bunnies {
                self.bunnybatch.add((bunny.position,));
            }
            for berry in &self.berries {
                self.bunnybatch.add((berry.position,));
            }
            graphics::draw(ctx, &self.berrybatch, (na::Point2::new(0.0, 0.0),))?;
            graphics::draw(ctx, &self.bunnybatch, (na::Point2::new(0.0, 0.0),))?;
            
        } else {
            for bunny in &self.bunnies {
                graphics::draw(ctx, &self.texture, (bunny.position,))?;
            }
            for bunny in &self.hoes {
                graphics::draw(ctx, &self.girl_texture, (bunny.position,))?;
            }
            for berry in &self.berries {
                graphics::draw(ctx, &self.berry_texture, (berry.position,))?;
            }
        }

        graphics::draw(ctx, &self.bottomline, (mint::Point2 { x: 0.0, y: 0.0 },))?;
        let score_box: graphics::Mesh = graphics::Mesh::new_rectangle(ctx, graphics::DrawMode::fill(), SCORE_BOX_FIELD, SCORE_BOX_COLOR)?;
        graphics::draw(ctx, &score_box, (mint::Point2 { x: 0.0, y: 0.0 },))?;

        let text_to_display: String;
        let text_location: na::Point2<f32> = na::Point2::new(0.0, 520.0);
        text_to_display = format!("M_SPD: {} M_LIB: {} M_RAD: {}",
        self.means[0], self.means[1], self.means[2]).to_string();
        let mut_text = graphics::Text::new(graphics::TextFragment{
            text: text_to_display,
            color: Some(graphics::BLACK),
            font: Some(graphics::Font::default()),
            scale: Some(graphics::Scale::uniform(30.0)),
        });
        graphics::draw(ctx, &mut_text, graphics::DrawParam::default().dest(text_location))?;

        let text_to_display: String;
        let text_location: na::Point2<f32> = na::Point2::new(0.0, 560.0);
        text_to_display = format!("F_SPD: {} F_LIB: {} F_RAD: {}",
        self.means[3], self.means[4], self.means[5]).to_string();
        let mut_text = graphics::Text::new(graphics::TextFragment{
            text: text_to_display,
            color: Some(graphics::BLACK),
            font: Some(graphics::Font::default()),
            scale: Some(graphics::Scale::uniform(30.0)),
        });
        graphics::draw(ctx, &mut_text, graphics::DrawParam::default().dest(text_location))?;

        graphics::set_window_title(
            ctx,
            &format!(
                "{} bunnies - {} girls - {:.0} FPS - m speed: {} - m libido: {} - m radius: {}",
                self.bunnies.len(),
                self.hoes.len(),
                timer::fps(ctx),
                self.means[0],
                self.means[1],
                self.means[2],
            ),
        );
        graphics::present(ctx)?;

        Ok(())
    }

    fn key_down_event(
        &mut self,
        _ctx: &mut Context,
        keycode: event::KeyCode,
        _keymods: event::KeyMods,
        _repeat: bool,
    ) {
        if keycode == event::KeyCode::Space {
            self.batched_drawing = !self.batched_drawing;
        }
        if keycode == event::KeyCode::LShift {
            let mut means : Vec<f32> = vec![0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
            for bunny in &self.bunnies{
                means[0] += bunny.speed;
                means[1] += bunny.libido;
                means[2] += bunny.radius;
            }
            for bunny in &self.hoes{
                means[3] += bunny.speed;
                means[4] += bunny.libido;
                means[5] += bunny.radius;
            }
            for i in 0..6{
                if i < 3{means[i] /= self.bunnies.len() as f32;}
                else {means[i] /= self.hoes.len() as f32;}
            }
            self.means = means;
        }
    }

    fn mouse_button_down_event(
        &mut self,
        _ctx: &mut Context,
        button: input::mouse::MouseButton,
        _x: f32,
        _y: f32,
    ) {
        if button == input::mouse::MouseButton::Left && self.click_timer == 0 {
            for _ in 0..INITIAL_BUNNIES {
                self.bunnies.push(Bunny::new(&mut self.rng, true));
            }
            self.click_timer = 10;
        }
    }
}

fn main() -> GameResult {
    let resource_dir = if let Ok(manifest_dir) = env::var("CARGO_MANIFEST_DIR") {
        let mut path = path::PathBuf::from(manifest_dir);
        path.push("resources");
        path
    } else {
        path::PathBuf::from("./resources")
    };

    let cb = ggez::ContextBuilder::new("bunnymark", "ggez").add_resource_path(resource_dir);
    let (ctx, event_loop) = &mut cb.build()?;

    let state = &mut GameState::new(ctx)?;
    event::run(ctx, event_loop, state)
}