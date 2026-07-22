import * as React from "react";

import { cn } from "@/lib/utils";

export function Input(props: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      {...props}
      className={cn(
        "h-11 w-full rounded-xl border border-zinc-300 bg-white px-3 text-sm outline-none transition-colors focus:border-brand-500 dark:border-zinc-700 dark:bg-zinc-900",
        props.className
      )}
    />
  );
}

