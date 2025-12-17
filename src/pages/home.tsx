import { Container, Row, Col } from 'react-bootstrap';
import Hero from '../components/hero';
import BlogCard from '../components/blogcard';
import { posts } from '../data/posts';

export default function Home() {
  return (
    <>
      <Hero />

      <Container className="my-5">
        <h2 className="mb-4 text-center">Latest Posts</h2>
        <Row className="g-4">
          {posts.map(post => (
            <Col md={4} key={post.id}>
              <BlogCard post={post} />
            </Col>
          ))}
        </Row>
      </Container>
    </>
  );
}