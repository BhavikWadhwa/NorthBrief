export const interestCategories = [
  { code: "local", label: "Local" },
  { code: "canada", label: "Canada" },
  { code: "world", label: "Global" },
  { code: "finance", label: "Finance" },
  { code: "global_finance", label: "Global Finance" },
  { code: "ai", label: "AI" },
  { code: "politics", label: "Politics" },
  { code: "war_conflict", label: "War & Conflict" },
  { code: "humanitarian", label: "Humanitarian" },
  { code: "wholesome", label: "Wholesome" },
  { code: "trending", label: "Trending" }
];

export const provinceOptions = [
  { code: "bc", label: "British Columbia" },
  { code: "ab", label: "Alberta" },
  { code: "on", label: "Ontario" },
  { code: "qc", label: "Quebec" }
];

export const citiesByProvince: Record<string, Array<{ code: string; label: string }>> = {
  bc: [
    { code: "vancouver", label: "Vancouver" },
    { code: "surrey", label: "Surrey" },
    { code: "abbotsford", label: "Abbotsford" },
    { code: "chilliwack", label: "Chilliwack" },
    { code: "maple_ridge", label: "Maple Ridge" },
    { code: "burnaby", label: "Burnaby" },
    { code: "kelowna", label: "Kelowna" },
    { code: "victoria", label: "Victoria" }
  ],
  ab: [
    { code: "calgary", label: "Calgary" },
    { code: "edmonton", label: "Edmonton" },
    { code: "red_deer", label: "Red Deer" },
    { code: "lethbridge", label: "Lethbridge" }
  ],
  on: [
    { code: "toronto", label: "Toronto" },
    { code: "ottawa", label: "Ottawa" },
    { code: "hamilton", label: "Hamilton" },
    { code: "london", label: "London" },
    { code: "mississauga", label: "Mississauga" }
  ],
  qc: [
    { code: "montreal", label: "Montreal" },
    { code: "quebec_city", label: "Quebec City" },
    { code: "gatineau", label: "Gatineau" },
    { code: "laval", label: "Laval" }
  ]
};

