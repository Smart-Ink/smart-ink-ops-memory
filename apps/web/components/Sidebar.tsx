import Link from 'next/link';

const items = [
  ['Dashboard', '/dashboard'],
  ['Memory search', '/memory'],
  ['Prompt library', '/prompts'],
  ['Tasks', '/tasks'],
  ['Meetings', '/meetings'],
  ['Review inbox', '/inbox'],
  ['Assets', '/assets'],
  ['Analytics', '/analytics']
];

export function Sidebar() {
  return (
    <aside className="sidebar">
      <h1>Smart Ink Ops</h1>
      <ul>
        {items.map(([label, href]) => (
          <li key={href}>
            <Link href={href}>{label}</Link>
          </li>
        ))}
      </ul>
    </aside>
  );
}
