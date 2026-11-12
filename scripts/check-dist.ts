// Asserts Insights is fully absent (expect=none) or fully present (expect=posts) in a built site.
// Usage: node scripts/check-dist.ts dist none|posts
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs'
import { join } from 'node:path'

function htmlFiles(dir: string): string[] {
  return readdirSync(dir).flatMap((n) => {
    const p = join(dir, n)
    return statSync(p).isDirectory() ? htmlFiles(p) : p.endsWith('.html') ? [p] : []
  })
}

export function problems(dist: string, expect: 'none' | 'posts'): string[] {
  const out: string[] = []
  const ins = join(dist, 'insights')
  const linking = htmlFiles(dist).filter((f) => readFileSync(f, 'utf8').includes('href="/insights/"'))
  if (expect === 'none') {
    if (existsSync(ins)) out.push('dist/insights/ exists but there are no visible posts')
    for (const f of linking) out.push(`${f} links to /insights/ but there are no visible posts`)
  } else {
    if (!existsSync(join(ins, 'index.html'))) out.push('missing insights/index.html')
    const posts = existsSync(ins) ? readdirSync(ins).filter((n) => existsSync(join(ins, n, 'index.html'))) : []
    if (posts.length === 0) out.push('no post pages under insights/')
    if (!existsSync(join(ins, 'rss.xml'))) out.push('missing insights/rss.xml')
    if (!existsSync(join(dist, 'index.html')) || !linking.some((f) => f === join(dist, 'index.html'))) out.push('home page has no Insights nav link')
  }
  return out
}

if (import.meta.main ?? process.argv[1]?.endsWith('check-dist.ts')) {
  const [dist = 'dist', expect = 'none'] = process.argv.slice(2)
  if (expect !== 'none' && expect !== 'posts') throw new Error('expect must be none|posts')
  const p = problems(dist, expect)
  for (const line of p) console.error(line)
  console.log(p.length ? `${p.length} problem(s)` : `Insights output OK (${expect})`)
  process.exit(p.length ? 1 : 0)
}
