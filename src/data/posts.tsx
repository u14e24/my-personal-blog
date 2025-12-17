export type Post = {
  id: string;
  title: string;
  excerpt: string;
};

export const posts: Post[] = [
  {
    id: 'welcome',
    title: 'Welcome to my blog',
    excerpt: 'Why I started writing…',
  },
  {
    id: 'react',
    title: 'Learning React',
    excerpt: 'My journey with React so far.',
  },
];