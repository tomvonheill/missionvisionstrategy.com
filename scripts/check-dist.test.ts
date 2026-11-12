import assert from 'node:assert/strict'
import { mkdirSync, mkdtempSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { describe, it } from 'node:test'
import { problems } from './check-dist.ts'

function site(files: Record<string, string>): string {
  const root = mkdtempSync(join(tmpdir(), 'dist-'))
  for (const [name, body] of Object.entries(files)) {
    mkdirSync(join(root, name, '..'), { recursive: true })
    writeFileSync(join(root, name), body)
  }
  return root
}

describe('problems(dist, "none")', () => {
  it('passes a site with no insights', () => {
    assert.deepEqual(problems(site({ 'index.html': '<a href="/services/">s</a>' }), 'none'), [])
  })
  it('flags an insights folder or a link to it', () => {
    const p = problems(site({ 'index.html': '<a href="/insights/">i</a>', 'insights/index.html': '' }), 'none')
    assert.equal(p.length, 2)
  })
})

describe('problems(dist, "posts")', () => {
  it('requires the index, at least one post, the feed and a nav link', () => {
    assert.equal(problems(site({ 'index.html': '' }), 'posts').length, 4)
    const ok = site({
      'index.html': '<a href="/insights/">Insights</a>',
      'insights/index.html': '', 'insights/a/index.html': '', 'insights/rss.xml': '',
    })
    assert.deepEqual(problems(ok, 'posts'), [])
  })
})

describe('draft tags', () => {
  const draft = '<span class="draft-tag">Draft</span>'
  it('flags a draft tag in either mode', () => {
    assert.equal(problems(site({ 'index.html': draft }), 'none').length, 1)
    const posts = site({
      'index.html': '<a href="/insights/">Insights</a>' + draft,
      'insights/index.html': '', 'insights/a/index.html': '', 'insights/rss.xml': '',
    })
    assert.equal(problems(posts, 'posts').length, 1)
  })
})
