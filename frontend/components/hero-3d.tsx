"use client";

import { motion, useMotionTemplate, useMotionValue, useSpring } from "framer-motion";
import Link from "next/link";

import { Button } from "@/components/ui/button";

export function Hero3D() {
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);
  const smoothX = useSpring(mouseX, { stiffness: 140, damping: 18 });
  const smoothY = useSpring(mouseY, { stiffness: 140, damping: 18 });
  const rotateX = useMotionTemplate`${smoothY}deg`;
  const rotateY = useMotionTemplate`${smoothX}deg`;

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_10%_20%,#91cfc1,transparent_35%),radial-gradient(circle_at_80%_10%,#9bc6ff,transparent_30%),#f4faf8] px-6 py-14 dark:bg-[radial-gradient(circle_at_10%_20%,#1f4b44,transparent_35%),radial-gradient(circle_at_80%_10%,#1f3658,transparent_30%),#090d10]">
      <div className="mx-auto grid max-w-6xl gap-10 md:grid-cols-2 md:items-center">
        <div>
          <p className="text-sm uppercase tracking-[0.2em] text-brand-700 dark:text-brand-200">NorthBrief</p>
          <h1 className="mt-4 max-w-2xl font-display text-5xl leading-tight text-zinc-900 dark:text-zinc-100">
            Briefings for busy people who still read the full story.
          </h1>
          <p className="mt-5 max-w-xl text-lg text-zinc-700 dark:text-zinc-300">
            Region-aware Canadian updates, neutral AI summaries, and direct links to original publishers.
          </p>
          <div className="mt-8 flex gap-3">
            <Link href="/signup">
              <Button>Get started</Button>
            </Link>
            <Link href="/signin">
              <Button variant="ghost">Sign in</Button>
            </Link>
          </div>
        </div>

        <motion.div
          onMouseMove={(event) => {
            const rect = event.currentTarget.getBoundingClientRect();
            const x = ((event.clientX - rect.left) / rect.width - 0.5) * 16;
            const y = ((event.clientY - rect.top) / rect.height - 0.5) * -16;
            mouseX.set(x);
            mouseY.set(y);
          }}
          onMouseLeave={() => {
            mouseX.set(0);
            mouseY.set(0);
          }}
          style={{ rotateX, rotateY, transformStyle: "preserve-3d" }}
          className="relative h-[360px] rounded-3xl border border-zinc-200/70 bg-white/60 p-6 shadow-xl backdrop-blur dark:border-zinc-700/80 dark:bg-zinc-900/50"
        >
          <motion.div
            style={{ transform: "translateZ(45px)" }}
            className="absolute left-6 top-6 rounded-xl bg-brand-600 px-3 py-1 text-xs text-white"
          >
            Live Briefing Card
          </motion.div>
          <motion.div
            style={{ transform: "translateZ(25px)" }}
            className="absolute left-6 top-16 right-6 rounded-2xl border border-zinc-200 bg-white p-5 shadow-md dark:border-zinc-700 dark:bg-zinc-900"
          >
            <h3 className="font-display text-xl">Transit disruptions expected across Metro Vancouver</h3>
            <p className="mt-3 text-sm text-zinc-600 dark:text-zinc-300">
              A planned labour action could affect commutes through next week while negotiations continue. Riders are
              being advised to check official schedules and contingency plans.
            </p>
            <p className="mt-3 text-xs text-zinc-500">Why this matters: Daily travel, local business traffic, and service planning may be disrupted.</p>
          </motion.div>
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            style={{ transform: "translateZ(70px)" }}
            className="absolute -bottom-4 -right-4 rounded-2xl bg-zinc-900 px-4 py-3 text-xs text-zinc-100 shadow-lg dark:bg-zinc-100 dark:text-zinc-900"
          >
            Source-linked • Region-aware • Fast
          </motion.div>
        </motion.div>
      </div>
    </main>
  );
}

