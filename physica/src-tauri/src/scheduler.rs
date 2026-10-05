use crate::model::{Problem, ProblemState, Settings};
use rand::Rng;
use std::collections::{HashMap, HashSet};
const FORMATS: [&str; 3] = ["Theory", "MCQ", "Experimental"];
pub fn format_lock(mode: &str) -> Option<&'static str> {
    FORMATS.into_iter().find(|format| *format == mode)
}
fn weighted<R: Rng + ?Sized>(weights: &[f64], rng: &mut R) -> usize {
    let mut r = rng.random::<f64>() * weights.iter().sum::<f64>();
    for (i, w) in weights.iter().enumerate() {
        r -= w;
        if r < 0. {
            return i;
        }
    }
    weights.len() - 1
}
/// A format draw is independent of its candidate count. Theory/MCQ known blocks use smoothed inverse exposure;
/// experiments use supply/(recent+4). Unknown-topic supply has its actual share, without inventing a classification.
pub fn draw<'a, R: Rng + ?Sized>(
    problems: &'a [Problem],
    states: &HashMap<String, ProblemState>,
    recent: &[String],
    settings: &Settings,
    rng: &mut R,
) -> Option<&'a Problem> {
    let locked_format = format_lock(&settings.mode);
    let by_id: HashMap<&str, &Problem> = problems
        .iter()
        .map(|p| (p.problem_id.as_str(), p))
        .collect();
    let canonical = |id: &str| {
        by_id
            .get(id)
            .and_then(|p| p.canonical_id.as_deref())
            .unwrap_or(id)
            .to_string()
    };
    let excluded: HashSet<String> = states
        .values()
        .filter(|s| s.skipped || (settings.exclude_solved && s.solved > 0))
        .map(|s| canonical(&s.problem_id))
        .collect();
    let seen_canonical: HashSet<String> = states
        .values()
        .filter(|s| s.opened > 0)
        .map(|s| canonical(&s.problem_id))
        .collect();
    let eligible: Vec<&Problem> = problems
        .iter()
        .filter(|p| {
            let seen = states.get(&p.problem_id).map(|s| s.opened).unwrap_or(0);
            p.decision.as_deref() == Some("KEEP")
                && p.available
                && p.format.is_some()
                && locked_format.is_none_or(|format| p.format.as_deref() == Some(format))
                && !excluded.contains(&canonical(&p.problem_id))
                && !(settings.mode == "Unseen"
                    && (seen > 0 || seen_canonical.contains(&canonical(&p.problem_id))))
                && (settings.mode != "Topic Focus"
                    || p.topic.is_some_and(|t| settings.topics.contains(&t)))
        })
        .collect();
    let eligible_ids: HashSet<&str> = eligible.iter().map(|p| p.problem_id.as_str()).collect();
    let eligible: Vec<_> = eligible
        .iter()
        .copied()
        .filter(|p| {
            !p.canonical_id
                .as_deref()
                .is_some_and(|id| eligible_ids.contains(id))
        })
        .collect();
    if eligible.is_empty() {
        return None;
    }
    let format = if let Some(format) = locked_format {
        format
    } else {
        let format_weights: Vec<f64> = FORMATS
            .iter()
            .enumerate()
            .map(|(i, f)| {
                if eligible.iter().any(|p| p.format.as_deref() == Some(f)) {
                    settings.weights[i]
                } else {
                    0.
                }
            })
            .collect();
        if format_weights.iter().sum::<f64>() <= 0. {
            return None;
        }
        FORMATS[weighted(&format_weights, rng)]
    };
    let pool: Vec<_> = eligible
        .into_iter()
        .filter(|p| p.format.as_deref() == Some(format))
        .collect();
    let pool = if pool.len() > 1 {
        pool.iter()
            .copied()
            .filter(|p| {
                recent
                    .first()
                    .is_none_or(|id| canonical(id) != canonical(&p.problem_id))
            })
            .collect()
    } else {
        pool
    };
    let mut supply = [0usize; 7];
    for p in &pool {
        supply[p.topic.unwrap_or(6)] += 1;
    }
    let mut exposure = [0f64; 7];
    for id in recent.iter().take(100) {
        if let Some(p) = by_id.get(id.as_str()) {
            if p.format.as_deref() == Some(format) {
                exposure[p.topic.unwrap_or(6)] += 1.;
            }
        }
    }
    let known = supply[..6].iter().sum::<usize>();
    let topic = if known == 0
        || (supply[6] > 0 && rng.random::<f64>() < (supply[6] as f64 / pool.len() as f64))
    {
        6
    } else {
        let ws: Vec<f64> = (0..6)
            .map(|i| {
                if supply[i] == 0 {
                    0.
                } else if format == "Experimental" {
                    supply[i] as f64 / (exposure[i] + 4.)
                } else {
                    1. / (exposure[i] + 2.)
                }
            })
            .collect();
        weighted(&ws, rng)
    };
    let bucket: Vec<_> = pool
        .into_iter()
        .filter(|p| p.topic.unwrap_or(6) == topic)
        .collect();
    let recent_ids: HashSet<_> = recent.iter().take(12).map(|id| canonical(id)).collect();
    let alternatives: Vec<_> = bucket
        .iter()
        .copied()
        .filter(|p| !recent_ids.contains(&canonical(&p.problem_id)))
        .collect();
    let bucket = if alternatives.is_empty() {
        bucket
    } else {
        alternatives
    };
    let weights: Vec<f64> = bucket
        .iter()
        .map(|p| {
            let n = states.get(&p.problem_id).map(|s| s.opened).unwrap_or(0) as f64;
            if n == 0. {
                1.6
            } else {
                1. / (1. + n * 0.35)
            }
        })
        .collect();
    Some(bucket[weighted(&weights, rng)])
}
#[cfg(test)]
mod tests {
    use super::*;
    use rand::SeedableRng;
    use rand_chacha::ChaCha8Rng;
    fn p(id: usize, format: &str, topic: usize) -> Problem {
        serde_json::from_value(serde_json::json!({"problem_id":id.to_string(),"title":"test","label":null,"competition":"test","year":null,"section":null,"format":format,"topic":topic,"secondary_topics":[],"pdf_path":"test.pdf","page_start":1,"page_end":1,"file_id":1,"source_problem_id":1,"solution":null,"available":true,"canonical_id":null,"decision":"KEEP","location":{},"source_quality_notes":null})).unwrap()
    }
    #[test]
    fn dedicated_modes_lock_format_even_with_zero_weight() {
        let ps: Vec<_> = FORMATS
            .iter()
            .enumerate()
            .flat_map(|(f, format)| (0..12).map(move |i| p(f * 12 + i, format, i % 6)))
            .collect();
        let mut rng = ChaCha8Rng::seed_from_u64(31);
        for (i, format) in FORMATS.iter().enumerate() {
            let mut cfg = Settings {
                mode: (*format).into(),
                ..Settings::default()
            };
            cfg.weights[i] = 0.; // Dedicated modes bypass all global format weights.
            for _ in 0..100 {
                assert_eq!(
                    draw(&ps, &HashMap::new(), &[], &cfg, &mut rng)
                        .unwrap()
                        .format
                        .as_deref(),
                    Some(*format)
                );
            }
        }
    }
    #[test]
    fn dedicated_modes_preserve_skip_solved_and_keep_eligibility() {
        let mut rng = ChaCha8Rng::seed_from_u64(32);
        for format in FORMATS {
            let mut ps = vec![
                p(0, format, 0),
                p(1, format, 0),
                p(2, format, 0),
                p(3, format, 0),
                p(4, format, 0),
            ];
            ps[3].decision = Some("BORDERLINE".into());
            ps[4].available = false;
            let states = HashMap::from([
                (
                    "0".into(),
                    ProblemState {
                        problem_id: "0".into(),
                        skipped: true,
                        ..Default::default()
                    },
                ),
                (
                    "1".into(),
                    ProblemState {
                        problem_id: "1".into(),
                        opened: 1,
                        solved: 1,
                        ..Default::default()
                    },
                ),
                (
                    "2".into(),
                    ProblemState {
                        problem_id: "2".into(),
                        opened: 1,
                        failed: 1,
                        ..Default::default()
                    },
                ),
            ]);
            let mut cfg = Settings {
                mode: format.into(),
                ..Settings::default()
            };
            let mut seen = HashSet::new();
            for _ in 0..100 {
                let id = &draw(&ps, &states, &[], &cfg, &mut rng).unwrap().problem_id;
                assert!(id == "1" || id == "2", "ineligible draw in {format}: {id}");
                seen.insert(id.clone());
            }
            assert!(seen.contains("1"), "Solved remains eligible in {format}");
            cfg.exclude_solved = true;
            for _ in 0..30 {
                assert_eq!(
                    draw(&ps, &states, &[], &cfg, &mut rng).unwrap().problem_id,
                    "2"
                );
            }
        }
    }
    #[test]
    fn dedicated_modes_empty_pool_never_falls_back() {
        let mut rng = ChaCha8Rng::seed_from_u64(33);
        for format in FORMATS {
            let cfg = Settings {
                mode: format.into(),
                exclude_solved: true,
                ..Settings::default()
            };
            let other: Vec<_> = FORMATS
                .iter()
                .filter(|f| **f != format)
                .enumerate()
                .map(|(i, f)| p(i + 1, f, 0))
                .collect();
            assert!(draw(&other, &HashMap::new(), &[], &cfg, &mut rng).is_none());
            let mut ps = other;
            ps.push(p(0, format, 0));
            for skipped in [true, false] {
                let states = HashMap::from([(
                    "0".into(),
                    ProblemState {
                        problem_id: "0".into(),
                        skipped,
                        solved: if skipped { 0 } else { 1 },
                        ..Default::default()
                    },
                )]);
                assert!(draw(&ps, &states, &[], &cfg, &mut rng).is_none());
            }
        }
    }
    #[test]
    fn dedicated_modes_share_topic_balance_supply_and_repeat_avoidance() {
        let mut rng = ChaCha8Rng::seed_from_u64(34);
        for format in FORMATS {
            let ps: Vec<_> = (0..120)
                .map(|i| {
                    p(
                        i,
                        format,
                        if format == "Experimental" {
                            if i < 108 {
                                0
                            } else {
                                1
                            }
                        } else {
                            i % 6
                        },
                    )
                })
                .collect();
            let cfg = Settings {
                mode: format.into(),
                ..Settings::default()
            };
            let mut counts = [0i32; 6];
            let mut recent = vec![];
            for _ in 0..1800 {
                let candidate = draw(&ps, &HashMap::new(), &recent, &cfg, &mut rng).unwrap();
                assert!(!recent.iter().take(12).any(|id| id == &candidate.problem_id));
                counts[candidate.topic.unwrap()] += 1;
                recent.insert(0, candidate.problem_id.clone());
                recent.truncate(100);
            }
            if format == "Experimental" {
                assert!(
                    counts[0] > 1260 && counts[0] < 1620,
                    "supply-aware {counts:?}"
                );
                assert!(counts[2..].iter().all(|count| *count == 0));
            } else {
                assert!(
                    counts.iter().all(|count| (*count - 300).abs() < 65),
                    "{format}: {counts:?}"
                );
            }
        }
    }
    #[test]
    fn eligibility_modes_and_tiny_pool() {
        let ps = vec![p(0, "Theory", 0), p(1, "Theory", 1), p(2, "Theory", 1)];
        let mut rng = ChaCha8Rng::seed_from_u64(4);
        let mut s = HashMap::new();
        s.insert(
            "0".into(),
            ProblemState {
                problem_id: "0".into(),
                skipped: true,
                ..Default::default()
            },
        );
        s.insert(
            "1".into(),
            ProblemState {
                problem_id: "1".into(),
                opened: 2,
                solved: 1,
                ..Default::default()
            },
        );
        let mut cfg = Settings::default();
        let mut seen = HashSet::new();
        for _ in 0..100 {
            seen.insert(
                draw(&ps, &s, &[], &cfg, &mut rng)
                    .unwrap()
                    .problem_id
                    .clone(),
            );
        }
        assert!(!seen.contains("0"));
        assert!(seen.contains("1"));
        cfg.exclude_solved = true;
        for _ in 0..20 {
            assert_eq!(draw(&ps, &s, &[], &cfg, &mut rng).unwrap().problem_id, "2");
        }
        cfg.exclude_solved = false;
        cfg.mode = "Unseen".into();
        assert_eq!(draw(&ps, &s, &[], &cfg, &mut rng).unwrap().problem_id, "2");
        cfg.mode = "Topic Focus".into();
        cfg.topics = vec![0];
        assert!(draw(&ps, &s, &[], &cfg, &mut rng).is_none());
        assert!(draw(&[], &s, &[], &cfg, &mut rng).is_none());
        cfg.mode = "Balanced".into();
        assert_eq!(
            draw(&ps[2..], &s, &["2".into()], &cfg, &mut rng)
                .unwrap()
                .problem_id,
            "2"
        );
    }
    #[test]
    fn format_weights_independent_of_supply() {
        let mut ps: Vec<_> = (0..1000).map(|i| p(i, "Theory", 0)).collect();
        ps.push(p(1000, "MCQ", 0));
        ps.push(p(1001, "Experimental", 0));
        let mut counts = [0; 3];
        let mut rng = ChaCha8Rng::seed_from_u64(9);
        for _ in 0..8000 {
            let f = draw(&ps, &HashMap::new(), &[], &Settings::default(), &mut rng)
                .unwrap()
                .format
                .as_deref()
                .unwrap();
            counts[FORMATS.iter().position(|x| *x == f).unwrap()] += 1;
        }
        assert!((counts[0] as i32 - 4000).abs() < 250);
        assert!((counts[1] as i32 - 2000).abs() < 200);
        assert!((counts[2] as i32 - 2000).abs() < 200);
    }
    #[test]
    fn aliases_and_immediate_repeats() {
        let mut ps = vec![p(0, "Theory", 0), p(1, "Theory", 1), p(2, "Theory", 0)];
        ps[2].canonical_id = Some("0".into());
        let mut rng = ChaCha8Rng::seed_from_u64(22);
        let mut states = HashMap::new();
        for _ in 0..30 {
            assert_eq!(
                draw(&ps, &states, &["0".into()], &Settings::default(), &mut rng)
                    .unwrap()
                    .problem_id,
                "1"
            );
        }
        states.insert(
            "2".into(),
            ProblemState {
                problem_id: "2".into(),
                skipped: true,
                ..Default::default()
            },
        );
        for _ in 0..30 {
            assert_eq!(
                draw(&ps, &states, &[], &Settings::default(), &mut rng)
                    .unwrap()
                    .problem_id,
                "1"
            );
        }
        ps[0].format = None;
        states.clear();
        let mut cfg = Settings::default();
        cfg.mode = "Topic Focus".into();
        cfg.topics = vec![0];
        assert_eq!(
            draw(&ps, &states, &[], &cfg, &mut rng).unwrap().problem_id,
            "2"
        );
    }
    #[test]
    fn topic_balance_repeat_avoidance_and_experimental_supply() {
        let ps: Vec<_> = (0..120).map(|i| p(i, "Theory", i % 6)).collect();
        let mut recent = vec![];
        let mut counts = [0; 6];
        let mut rng = ChaCha8Rng::seed_from_u64(7);
        for _ in 0..3000 {
            let p = draw(
                &ps,
                &HashMap::new(),
                &recent,
                &Settings::default(),
                &mut rng,
            )
            .unwrap();
            assert!(!recent.iter().take(12).any(|id| id == &p.problem_id));
            counts[p.topic.unwrap()] += 1;
            recent.insert(0, p.problem_id.clone());
            recent.truncate(100);
        }
        assert!(counts.iter().all(|c| (*c as i32 - 500).abs() < 80));
        let ps: Vec<_> = (0..100)
            .map(|i| p(i, "Experimental", if i < 90 { 0 } else { 1 }))
            .collect();
        let mut a = 0;
        let mut recent = vec![];
        for _ in 0..3000 {
            let p = draw(
                &ps,
                &HashMap::new(),
                &recent,
                &Settings::default(),
                &mut rng,
            )
            .unwrap();
            a += (p.topic == Some(0)) as i32;
            recent.insert(0, p.problem_id.clone());
            recent.truncate(100);
        }
        assert!(a > 2100 && a < 2700, "supply-aware draws: {a}");
    }
}
