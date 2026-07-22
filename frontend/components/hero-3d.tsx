"use client";

import {
  ArrowRight,
  Bookmark,
  Check,
  Clock3,
  ExternalLink,
  MapPin,
  Radio,
  ShieldCheck,
  Sparkles
} from "lucide-react";
import { motion, useMotionTemplate, useMotionValue, useReducedMotion, useSpring } from "framer-motion";
import Link from "next/link";

const sources = ["CBC News", "Global News", "CTV News", "CityNews", "Government of Canada", "BBC World"];

const lenses = [
  {
    number: "01",
    title: "Close to home",
    copy: "City and province signals rise first, so a transit change in Vancouver does not get buried under national headlines.",
    icon: MapPin,
    tone: "bg-[#dcebe5] text-[#174d46]"
  },
  {
    number: "02",
    title: "Built around you",
    copy: "Choose the beats you care about. Your briefing stays preference-led without building an invasive behaviour profile.",
    icon: Sparkles,
    tone: "bg-[#f5dfb8] text-[#713f12]"
  },
  {
    number: "03",
    title: "Open to the source",
    copy: "Every summary names its publisher and points to the original reporting. NorthBrief is the start, not the substitute.",
    icon: ExternalLink,
    tone: "bg-[#e6e2f1] text-[#403366]"
  }
];

const regions = [
  { name: "British Columbia", signal: "Housing", position: "left-[13%] top-[47%]" },
  { name: "Alberta", signal: "Energy", position: "left-[29%] top-[50%]" },
  { name: "Ontario", signal: "Economy", position: "left-[61%] top-[59%]" },
  { name: "Quebec", signal: "Politics", position: "left-[73%] top-[48%]" },
  { name: "Atlantic", signal: "Weather", position: "right-[5%] top-[58%]" }
];

const reveal = {
  hidden: { opacity: 0, y: 22 },
  visible: { opacity: 1, y: 0 }
};

export function Hero3D() {
  const reduceMotion = useReducedMotion();
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);
  const smoothX = useSpring(mouseX, { stiffness: 120, damping: 18 });
  const smoothY = useSpring(mouseY, { stiffness: 120, damping: 18 });
  const rotateX = useMotionTemplate`${smoothY}deg`;
  const rotateY = useMotionTemplate`${smoothX}deg`;

  return (
    <main className="overflow-hidden bg-[#f5f1e8] text-[#102529] dark:bg-[#091315] dark:text-[#f4f0e6]">
      <section className="relative min-h-[760px] border-b border-[#102529]/10 px-5 pb-24 pt-5 sm:px-8 lg:px-12">
        <div className="pointer-events-none absolute inset-0 opacity-[0.18] [background-image:linear-gradient(to_right,#224b4e_1px,transparent_1px),linear-gradient(to_bottom,#224b4e_1px,transparent_1px)] [background-size:42px_42px] dark:opacity-[0.08]" />
        <div className="pointer-events-none absolute -right-40 -top-40 h-[520px] w-[520px] rounded-full border-[90px] border-[#d7e6df]/70 dark:border-[#153237]" />

        <nav className="relative z-20 mx-auto flex max-w-7xl items-center justify-between rounded-full border border-[#102529]/10 bg-[#faf7f0]/80 px-5 py-3 backdrop-blur-xl dark:border-white/10 dark:bg-[#0d1d20]/80">
          <Link href="/" className="flex items-center gap-2 font-display text-xl font-semibold tracking-[-0.04em]">
            <span className="grid h-7 w-7 place-items-center rounded-full bg-[#174d46] text-xs font-bold text-white">N</span>
            NorthBrief
          </Link>
          <div className="hidden items-center gap-7 text-sm font-medium md:flex">
            <a href="#why" className="transition hover:text-[#2e7f74]">Why NorthBrief</a>
            <a href="#coverage" className="transition hover:text-[#2e7f74]">Coverage</a>
            <a href="#trust" className="transition hover:text-[#2e7f74]">Our approach</a>
          </div>
          <div className="flex items-center gap-2">
            <Link href="/signin" className="hidden rounded-full px-4 py-2 text-sm font-semibold transition hover:bg-black/5 sm:block dark:hover:bg-white/10">
              Sign in
            </Link>
            <Link href="/signup" className="rounded-full bg-[#102529] px-5 py-2.5 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:bg-[#174d46] dark:bg-[#f4f0e6] dark:text-[#102529]">
              Build my brief
            </Link>
          </div>
        </nav>

        <div className="relative z-10 mx-auto grid max-w-7xl gap-16 pt-20 lg:grid-cols-[1.08fr_0.92fr] lg:items-center lg:pt-28">
          <motion.div initial="hidden" animate="visible" transition={{ staggerChildren: 0.1 }}>
            <motion.div variants={reveal} transition={{ duration: 0.55 }} className="inline-flex items-center gap-2 rounded-full border border-[#174d46]/20 bg-[#dcebe5]/70 px-3 py-1.5 text-xs font-bold uppercase tracking-[0.16em] text-[#174d46] dark:bg-[#174d46]/20 dark:text-[#9ed2c7]">
              <Radio className="h-3.5 w-3.5" /> Canada, in context
            </motion.div>
            <motion.h1 variants={reveal} transition={{ duration: 0.65 }} className="mt-7 max-w-3xl font-display text-[clamp(3.5rem,7vw,6.7rem)] font-semibold leading-[0.88] tracking-[-0.07em]">
              Know what matters.
              <span className="mt-2 block font-normal italic text-[#d94f3d]">Keep your morning.</span>
            </motion.h1>
            <motion.p variants={reveal} transition={{ duration: 0.65 }} className="mt-8 max-w-xl text-lg leading-8 text-[#3d5255] dark:text-[#b9c8c9]">
              A calm, region-aware briefing that turns the day&apos;s Canadian news into clear summaries, then sends you to the journalism behind them.
            </motion.p>
            <motion.div variants={reveal} transition={{ duration: 0.65 }} className="mt-9 flex flex-col gap-3 sm:flex-row">
              <Link href="/signup" className="group inline-flex items-center justify-center gap-2 rounded-full bg-[#d94f3d] px-6 py-3.5 text-sm font-bold text-white shadow-[0_12px_35px_rgba(217,79,61,0.25)] transition hover:-translate-y-1 hover:bg-[#c74231]">
                Create your briefing <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
              </Link>
              <Link href="/signin" className="inline-flex items-center justify-center rounded-full border border-[#102529]/20 px-6 py-3.5 text-sm font-bold transition hover:bg-white/60 dark:border-white/20 dark:hover:bg-white/10">
                I already have an account
              </Link>
            </motion.div>
            <motion.div variants={reveal} className="mt-8 flex flex-wrap gap-x-6 gap-y-2 text-xs font-semibold text-[#5b6d70] dark:text-[#92a7aa]">
              <span className="flex items-center gap-1.5"><Check className="h-3.5 w-3.5 text-[#2e7f74]" /> No paywall added</span>
              <span className="flex items-center gap-1.5"><Check className="h-3.5 w-3.5 text-[#2e7f74]" /> Original sources linked</span>
              <span className="flex items-center gap-1.5"><Check className="h-3.5 w-3.5 text-[#2e7f74]" /> Preference-led</span>
            </motion.div>
          </motion.div>

          <div className="relative mx-auto w-full max-w-[560px] [perspective:1200px]">
            <motion.div
              onMouseMove={(event) => {
                if (reduceMotion) return;
                const rect = event.currentTarget.getBoundingClientRect();
                mouseX.set(((event.clientX - rect.left) / rect.width - 0.5) * 9);
                mouseY.set(((event.clientY - rect.top) / rect.height - 0.5) * -9);
              }}
              onMouseLeave={() => {
                mouseX.set(0);
                mouseY.set(0);
              }}
              initial={{ opacity: 0, y: 28, rotate: 2 }}
              animate={{ opacity: 1, y: 0, rotate: 0 }}
              transition={{ duration: 0.8, delay: 0.15 }}
              style={reduceMotion ? undefined : { rotateX, rotateY, transformStyle: "preserve-3d" }}
              className="relative rounded-[2rem] border border-[#102529]/10 bg-[#fffdf8] p-3 shadow-[0_30px_80px_rgba(25,57,60,0.2)] dark:border-white/10 dark:bg-[#102326]"
            >
              <div className="relative h-52 overflow-hidden rounded-[1.4rem] bg-[#193a3d] p-6 text-white">
                <div className="absolute -right-12 -top-20 h-64 w-64 rounded-full border-[52px] border-[#39766e]" />
                <div className="absolute bottom-0 left-0 h-20 w-full bg-gradient-to-t from-black/25 to-transparent" />
                <div className="relative flex items-start justify-between text-xs font-bold uppercase tracking-[0.14em]">
                  <span className="rounded-full bg-white/15 px-3 py-1.5 backdrop-blur">Local signal</span>
                  <span className="flex items-center gap-1.5"><MapPin className="h-3.5 w-3.5" /> Vancouver, BC</span>
                </div>
                <div className="absolute bottom-6 left-6 right-6">
                  <p className="text-xs text-white/65">Your morning briefing</p>
                  <p className="mt-1 font-display text-2xl font-semibold tracking-tight">Wednesday, 7:42 AM</p>
                </div>
              </div>
              <div className="p-5 sm:p-6">
                <div className="flex items-center justify-between text-xs font-bold uppercase tracking-[0.12em] text-[#d94f3d]">
                  <span>Housing</span>
                  <span className="flex items-center gap-1.5 normal-case tracking-normal text-[#738386]"><Clock3 className="h-3.5 w-3.5" /> 8 min ago</span>
                </div>
                <h2 className="mt-4 font-display text-2xl font-semibold leading-tight tracking-[-0.03em]">New housing targets put Metro Vancouver approvals in focus</h2>
                <p className="mt-4 text-sm leading-6 text-[#526568] dark:text-[#afbec0]">Municipalities face updated timelines as the province tracks permits and multi-unit construction. The next reporting cycle will show where approvals are accelerating and where gaps remain.</p>
                <div className="mt-5 border-l-2 border-[#e8bd69] pl-4 text-sm leading-6 text-[#3d5255] dark:text-[#c5d0d1]">
                  <strong>Why it matters:</strong> Housing supply decisions made now shape rents, commutes, and neighbourhood growth.
                </div>
                <div className="mt-6 flex items-center justify-between border-t border-[#102529]/10 pt-4 dark:border-white/10">
                  <div>
                    <p className="text-xs text-[#738386]">Reported by</p>
                    <p className="mt-0.5 text-sm font-bold">CBC News</p>
                  </div>
                  <div className="flex gap-2">
                    <button aria-label="Save sample story" className="grid h-10 w-10 place-items-center rounded-full border border-[#102529]/10 transition hover:bg-[#f5f1e8] dark:border-white/10 dark:hover:bg-white/10"><Bookmark className="h-4 w-4" /></button>
                    <span className="grid h-10 w-10 place-items-center rounded-full bg-[#102529] text-white dark:bg-[#f4f0e6] dark:text-[#102529]"><ArrowRight className="h-4 w-4" /></span>
                  </div>
                </div>
              </div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.8, duration: 0.5 }}
              className="absolute -right-2 top-28 hidden rounded-2xl border border-white/70 bg-white/90 px-4 py-3 shadow-xl backdrop-blur sm:block dark:border-white/10 dark:bg-[#173033]/90"
            >
              <p className="text-[10px] font-bold uppercase tracking-[0.14em] text-[#718184]">Signal match</p>
              <p className="mt-1 font-display text-lg font-semibold text-[#174d46] dark:text-[#9ed2c7]">BC + Housing</p>
            </motion.div>
          </div>
        </div>
      </section>

      <section className="border-b border-[#102529]/10 bg-[#fffdf8] py-6 dark:border-white/10 dark:bg-[#0d1d20]">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 px-5 sm:px-8 lg:flex-row lg:items-center lg:px-12">
          <p className="shrink-0 text-xs font-bold uppercase tracking-[0.18em] text-[#738386]">Briefings link out to</p>
          <div className="flex flex-wrap items-center gap-x-7 gap-y-3 lg:ml-auto lg:justify-end">
            {sources.map((source) => <span key={source} className="font-display text-sm font-semibold text-[#344b4e] dark:text-[#b7c6c8]">{source}</span>)}
          </div>
        </div>
      </section>

      <section id="why" className="px-5 py-24 sm:px-8 lg:px-12 lg:py-32">
        <div className="mx-auto max-w-7xl">
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }} variants={reveal} transition={{ duration: 0.6 }} className="grid gap-8 lg:grid-cols-2">
            <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#d94f3d]">A better signal-to-noise ratio</p>
            <h2 className="font-display text-4xl font-semibold leading-[1.05] tracking-[-0.05em] sm:text-6xl">The national picture, without losing your street.</h2>
          </motion.div>
          <div className="mt-16 grid gap-5 md:grid-cols-3">
            {lenses.map((lens, index) => {
              const Icon = lens.icon;
              return (
                <motion.article key={lens.title} initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.25 }} variants={reveal} transition={{ duration: 0.5, delay: index * 0.1 }} className="group rounded-[1.75rem] border border-[#102529]/10 bg-[#fffdf8] p-7 transition duration-300 hover:-translate-y-2 hover:shadow-[0_22px_50px_rgba(29,63,60,0.12)] dark:border-white/10 dark:bg-[#102326]">
                  <div className="flex items-center justify-between">
                    <span className={`grid h-12 w-12 place-items-center rounded-2xl ${lens.tone}`}><Icon className="h-5 w-5" /></span>
                    <span className="font-display text-sm text-[#829092]">{lens.number}</span>
                  </div>
                  <h3 className="mt-10 font-display text-2xl font-semibold tracking-[-0.03em]">{lens.title}</h3>
                  <p className="mt-4 text-sm leading-7 text-[#596b6e] dark:text-[#aebdbf]">{lens.copy}</p>
                </motion.article>
              );
            })}
          </div>
        </div>
      </section>

      <section id="coverage" className="bg-[#102529] px-5 py-24 text-[#f8f4eb] sm:px-8 lg:px-12 lg:py-32">
        <div className="mx-auto grid max-w-7xl gap-16 lg:grid-cols-[0.7fr_1.3fr] lg:items-center">
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }} variants={reveal}>
            <p className="text-xs font-bold uppercase tracking-[0.2em] text-[#e8bd69]">Coverage that knows where you are</p>
            <h2 className="mt-6 font-display text-4xl font-semibold leading-[1.03] tracking-[-0.05em] sm:text-5xl">From your city to the world in one scroll.</h2>
            <p className="mt-6 max-w-lg leading-7 text-[#b5c3c5]">NorthBrief combines publisher metadata, region rules, and topic signals to surface nearby stories first while preserving the larger Canadian and global context.</p>
            <div className="mt-9 grid grid-cols-3 gap-3">
              <div className="rounded-2xl border border-white/10 p-4"><strong className="font-display text-2xl">City</strong><span className="mt-1 block text-xs text-[#91a5a8]">Metro relevance</span></div>
              <div className="rounded-2xl border border-white/10 p-4"><strong className="font-display text-2xl">Province</strong><span className="mt-1 block text-xs text-[#91a5a8]">Regional impact</span></div>
              <div className="rounded-2xl border border-white/10 p-4"><strong className="font-display text-2xl">Canada</strong><span className="mt-1 block text-xs text-[#91a5a8]">National context</span></div>
            </div>
          </motion.div>

          <motion.div initial={{ opacity: 0, scale: 0.96 }} whileInView={{ opacity: 1, scale: 1 }} viewport={{ once: true, amount: 0.25 }} transition={{ duration: 0.7 }} className="relative min-h-[420px] overflow-hidden rounded-[2rem] border border-white/10 bg-[#153337] p-7 sm:min-h-[500px]">
            <div className="absolute inset-[12%] rounded-[50%] border border-white/10" />
            <div className="absolute inset-[22%] rounded-[50%] border border-white/10" />
            <div className="absolute inset-[32%] rounded-[50%] border border-white/10" />
            <div className="absolute left-[8%] top-[25%] h-[45%] w-[82%] rotate-[-5deg] rounded-[48%_52%_38%_62%/60%_45%_55%_40%] border-2 border-[#5d8e86]/40 bg-[#1b4548]/60" />
            <div className="relative flex items-center justify-between">
              <div><p className="text-xs font-bold uppercase tracking-[0.16em] text-[#90aaa7]">Live relevance map</p><p className="mt-1 font-display text-xl font-semibold">Canada</p></div>
              <span className="flex items-center gap-2 rounded-full bg-[#d94f3d] px-3 py-1.5 text-xs font-bold"><span className="h-1.5 w-1.5 animate-pulse rounded-full bg-white" /> Signals active</span>
            </div>
            {regions.map((region, index) => (
              <motion.div key={region.name} initial={{ opacity: 0, scale: 0.6 }} whileInView={{ opacity: 1, scale: 1 }} viewport={{ once: true }} transition={{ delay: 0.35 + index * 0.1 }} className={`absolute ${region.position}`}>
                <span className="relative flex h-4 w-4">
                  <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-[#e8bd69] opacity-40" />
                  <span className="relative inline-flex h-4 w-4 rounded-full border-4 border-[#153337] bg-[#e8bd69]" />
                </span>
                <div className="mt-2 rounded-xl border border-white/10 bg-[#0f2629]/90 px-3 py-2 shadow-lg backdrop-blur">
                  <p className="whitespace-nowrap text-xs font-bold">{region.name}</p>
                  <p className="mt-0.5 text-[10px] text-[#94aaad]">{region.signal} trending</p>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      <section id="trust" className="px-5 py-24 sm:px-8 lg:px-12 lg:py-32">
        <div className="mx-auto grid max-w-7xl gap-12 lg:grid-cols-[0.85fr_1.15fr] lg:items-start">
          <div className="lg:sticky lg:top-20">
            <span className="grid h-14 w-14 place-items-center rounded-2xl bg-[#dcebe5] text-[#174d46]"><ShieldCheck className="h-6 w-6" /></span>
            <h2 className="mt-7 font-display text-4xl font-semibold tracking-[-0.05em] sm:text-5xl">Brief, not borrowed.</h2>
            <p className="mt-5 max-w-md leading-7 text-[#596b6e] dark:text-[#aebdbf]">We design every card to help you orient quickly and continue to the original publisher when a story deserves your time.</p>
          </div>
          <div className="divide-y divide-[#102529]/10 border-y border-[#102529]/10 dark:divide-white/10 dark:border-white/10">
            {[
              ["01", "Metadata in", "Headlines, permitted snippets, publication times, and source links enter the pipeline."],
              ["02", "Context added", "Region and category signals organize the story without changing what the source reported."],
              ["03", "A restrained brief", "Concise summaries are checked for length and uncertainty, with weak inputs flagged for review."],
              ["04", "Journalism one tap away", "The publisher and canonical link stay visible on every card, every time."]
            ].map(([number, title, copy], index) => (
              <motion.div key={number} initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.5 }} variants={reveal} transition={{ delay: index * 0.06 }} className="grid gap-3 py-7 sm:grid-cols-[56px_180px_1fr] sm:items-start">
                <span className="font-display text-sm text-[#d94f3d]">{number}</span>
                <h3 className="font-display text-lg font-semibold">{title}</h3>
                <p className="text-sm leading-6 text-[#607174] dark:text-[#aebdbf]">{copy}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="px-5 pb-8 sm:px-8 lg:px-12">
        <div className="relative mx-auto max-w-7xl overflow-hidden rounded-[2.25rem] bg-[#d94f3d] px-7 py-16 text-white sm:px-12 lg:px-16 lg:py-20">
          <div className="absolute -right-20 -top-32 h-96 w-96 rounded-full border-[65px] border-white/10" />
          <div className="relative grid gap-10 lg:grid-cols-[1fr_auto] lg:items-end">
            <div>
              <p className="text-xs font-bold uppercase tracking-[0.2em] text-white/70">Your news. Better ordered.</p>
              <h2 className="mt-5 max-w-3xl font-display text-4xl font-semibold leading-[1.02] tracking-[-0.05em] sm:text-6xl">Make room for context, not clutter.</h2>
            </div>
            <Link href="/signup" className="group inline-flex w-fit items-center gap-3 rounded-full bg-white px-6 py-3.5 text-sm font-bold text-[#102529] transition hover:-translate-y-1">
              Start my NorthBrief <ArrowRight className="h-4 w-4 transition group-hover:translate-x-1" />
            </Link>
          </div>
        </div>
      </section>

      <footer className="px-5 py-10 sm:px-8 lg:px-12">
        <div className="mx-auto flex max-w-7xl flex-col gap-5 border-t border-[#102529]/10 pt-8 text-sm text-[#66777a] sm:flex-row sm:items-center sm:justify-between dark:border-white/10">
          <p className="font-display font-semibold text-[#102529] dark:text-[#f4f0e6]">NorthBrief <span className="font-body font-normal text-[#728184]">News with a sense of place.</span></p>
          <div className="flex gap-6"><Link href="/signin" className="hover:text-[#102529] dark:hover:text-white">Sign in</Link><Link href="/signup" className="hover:text-[#102529] dark:hover:text-white">Create account</Link></div>
        </div>
      </footer>
    </main>
  );
}
