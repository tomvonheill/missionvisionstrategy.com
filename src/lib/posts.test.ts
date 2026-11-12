import assert from 'node:assert/strict'
import { describe, it } from 'node:test'
import { formatDate, isVisible, newestFirst } from './posts.ts'

const post = (id: string, iso: string, draft = false) => ({ id, data: { pubDate: new Date(iso), draft } })

describe('isVisible', () => {
  it('hides drafts unless drafts are included', () => {
    assert.equal(isVisible({ draft: true }, false), false)
    assert.equal(isVisible({ draft: true }, true), true)
    assert.equal(isVisible({ draft: false }, false), true)
  })
})

describe('newestFirst', () => {
  it('sorts by pubDate descending, ties by id, without mutating', () => {
    const input = [post('b', '2026-01-01'), post('c', '2026-03-01'), post('a', '2026-01-01')]
    assert.deepEqual(newestFirst(input).map((p) => p.id), ['c', 'a', 'b'])
    assert.deepEqual(input.map((p) => p.id), ['b', 'c', 'a'])
  })
  it('returns an empty list for no posts', () => {
    assert.deepEqual(newestFirst([]), [])
  })
})

describe('formatDate', () => {
  it('formats as Month day, year in UTC', () => {
    assert.equal(formatDate(new Date('2026-11-12T00:00:00Z')), 'November 12, 2026')
    assert.equal(formatDate(new Date('2026-01-01T23:30:00Z')), 'January 1, 2026')
  })
})
