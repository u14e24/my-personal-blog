import { Card, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import type { Post } from '../data/posts';

export default function BlogCard({ post }: { post: Post }) {
  return (
    <Card className="h-100 shadow-sm">
  <Card.Body>
        <Card.Title>{post.title}</Card.Title>
        <Card.Text>{post.excerpt}</Card.Text>
        <Button as={Link as any} to={`/blog/${post.id}`} variant="primary">
          Read more
        </Button>
      </Card.Body>
    </Card>
  );
}