---
name: web-performance-and-bundling
description: Use when measuring or improving Web Vitals (LCP, CLS, INP), reducing bundle size, adding code splitting and lazy loading, setting performance budgets in CI, or optimizing React rendering (memoization, virtualization, Suspense). Covers Lighthouse, bundle analysis, SSR/SSG tradeoffs, and the principle of measuring before optimizing.
family: method
profile_level: Senior+
---

# Web Performance and Bundling

## Purpose

Make the application fast for users on the target device and network. Measure first; optimize where the data says it matters. Never add architectural complexity for a performance win that has not been measured.

## Use When

- Core Web Vitals (LCP, CLS, INP) are failing or regressing.
- Bundle size exceeds the project's performance budget.
- A page or route is loading noticeably slowly and Lighthouse or user timing confirms it.
- Adding lazy loading or code splitting to a route or heavy component.
- Setting up performance budget enforcement in CI (Lighthouse CI, bundlesize, size-limit).
- Reviewing whether a memoization, virtualization, or SSR decision is warranted.

## Do Not Use When

- The task is API loading state handling → `api-integration-frontend`.
- The task is state invalidation and re-fetch strategy → `state-management-and-data-flow`.
- The task is test coverage of rendered components → `frontend-testing`.

## Inputs

- Lighthouse report or Web Vitals field data (CrUX / RUM).
- Webpack/Vite bundle analysis (source-map-explorer, rollup-plugin-visualizer).
- React Profiler flamegraph for rendering hotspots.
- Performance budget (if defined) or project SLA for page load.

## Workflow

1. **Measure before acting.** Run Lighthouse in CI against a production-equivalent build. Collect LCP, CLS, INP. Record a baseline. Optimizations without a baseline produce invisible wins.

2. **Identify the bottleneck category:**
   - Network: large JS bundles, unoptimized images, render-blocking resources.
   - Rendering: excessive re-renders, synchronous long tasks blocking the main thread.
   - Layout shift: images without dimensions, late-injected content, font swap.

3. **Network — bundle reduction:**
   - Open the bundle analyser (rollup-plugin-visualizer or webpack-bundle-analyzer). Find the largest modules.
   - Apply route-level code splitting first: `const Page = lazy(() => import('./pages/HeavyPage'))`.
   - Apply component-level splitting for modal, drawer, chart, or editor components not needed on initial render.
   - Check for accidental full-library imports (`import _ from 'lodash'` instead of named imports).
   - Set a `bundlesize` or `size-limit` config to enforce a budget in CI. Fail the build when the limit is exceeded.

4. **Rendering — React-specific:**
   - Use React Profiler to find components that re-render without visible reason.
   - Apply `useMemo`, `useCallback`, or `React.memo` only where profiling shows a measurable win. Do not apply them preemptively.
   - For long lists (>100 items), apply windowing: `react-virtual` / `TanStack Virtual`.
   - For expensive computations in the render path: move to a worker or memoize with a stable key.

5. **Layout shift:**
   - Always specify `width` and `height` attributes on `<img>` or use `aspect-ratio` in CSS.
   - Prefer `font-display: optional` or `font-display: swap` with a system font fallback.
   - Avoid injecting content above the fold after first paint.

6. **SSR/SSG decision:**
   - Static pages or data that changes infrequently → SSG (Next.js `getStaticProps` / `generateStaticParams`).
   - Personalized pages with user-specific data → SSR or client-side with a skeleton.
   - Do not reach for SSR to fix a large bundle — fix the bundle first.

7. Document performance changes in the PR: before/after Lighthouse scores, bundle delta, and the specific optimization applied.

## Outputs

- Lighthouse CI config with passing budgets for LCP, CLS, INP.
- Bundle analyser report with identified and resolved large dependencies.
- Code splitting applied to routes and heavy components.
- React Profiler evidence for memoization decisions.
- `size-limit` or `bundlesize` config in the repo.

## Named Patterns

### Good — Route-level lazy loading
```tsx
import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';

const DashboardPage = lazy(() => import('./pages/DashboardPage'));
const ReportsPage   = lazy(() => import('./pages/ReportsPage'));

export function AppRoutes() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/reports"   element={<ReportsPage />} />
      </Routes>
    </Suspense>
  );
}
```
Each route loads its JS only when the user navigates to it. Initial bundle is reduced.

### Bad — All routes imported eagerly
```tsx
import DashboardPage from './pages/DashboardPage';
import ReportsPage   from './pages/ReportsPage';
import AnalyticsPage from './pages/AnalyticsPage';
// All JS loads on first visit regardless of which route the user needs
```

### Good — Measured memoization
```tsx
// React Profiler shows ProductCard re-renders 800× in a list of 200 items
// because the parent passes a new callback reference on every render.

const handleSelect = useCallback((id: string) => onSelect(id), [onSelect]);
const MemoProductCard = React.memo(ProductCard);
// After: ProductCard renders only when its props change
```
Profiler evidence precedes the optimization.

### Bad — Preemptive `useMemo` everywhere
```tsx
const title = useMemo(() => item.name.trim(), [item.name]);
// String operation takes <0.01 ms; useMemo overhead is comparable
```

### Good — Image with explicit dimensions
```tsx
<img
  src="/hero.webp"
  width={1200}
  height={600}
  alt="Product hero"
  loading="lazy"
/>
```
Browser reserves space before the image loads; CLS is zero for this element.

### Bad — Image without dimensions
```tsx
<img src="/hero.webp" alt="Product hero" />
// Height unknown until image loads; surrounding content shifts → CLS penalty
```

### Good — Bundlesize CI gate
```json
// .bundlesize.config.json
{
  "files": [
    { "path": "./dist/assets/index-*.js", "maxSize": "150 kB" },
    { "path": "./dist/assets/vendor-*.js", "maxSize": "300 kB" }
  ]
}
```
Build fails if a dependency update inflates the bundle beyond budget.

## Boundaries

- Owns frontend-side performance measurement and optimization.
- Does not own backend response time, CDN configuration, or server-side caching → `devops-sre`.
- Does not own infrastructure SSR deployment → `devops-sre` / `system-architect`.
- Does not own API response shape and payload size → `backend-go-developer` / `python-developer`.

## Sources

### Priority 1 — Web performance canon
- Web Vitals — https://web.dev/vitals/
- MDN: Performance — https://developer.mozilla.org/en-US/docs/Web/Performance
- React docs: Performance — https://react.dev/reference/react/memo

### Priority 2 — Tools and orientation
- Lighthouse documentation — https://developer.chrome.com/docs/lighthouse/
- Webpack Bundle Analyzer — https://github.com/webpack-contrib/webpack-bundle-analyzer
- rollup-plugin-visualizer — https://github.com/btd/rollup-plugin-visualizer

### Priority 3 — Pattern background
- web.dev: Optimize loading performance — https://web.dev/fast/

## Handoff

- Backend payload size and response time → `backend-go-developer` / `python-developer`.
- CDN, caching, and SSR infra → `devops-sre`.
- React rendering architecture (component decomposition) → `frontend-architecture-and-component-design`.
- User-visible performance targets (business SLA) → `product-manager` / `system-analyst`.
