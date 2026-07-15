<?php
/**
 * Bricks Dynamic Tag: {author_first_initial}
 * Returns the first letter of the post author's display name (uppercase).
 *
 * Register in Bricks builder and render on frontend.
 * Lightweight: fires only when Bricks encounters this specific tag.
 */

add_filter( 'bricks/dynamic_tags_list', 'dtl_register_author_first_initial_tag' );

function dtl_register_author_first_initial_tag( $tags ) {
	$tags[] = [
		'name'  => '{author_first_initial}',
		'label' => 'Author First Initial',
		'group' => 'Author',
	];
	return $tags;
}

add_filter( 'bricks/dynamic_data/render_tag', 'dtl_render_author_first_initial', 20, 3 );

function dtl_render_author_first_initial( $tag, $post, $context = 'text' ) {
	if ( ! is_string( $tag ) ) {
		return $tag;
	}

	$clean_tag = str_replace( [ '{', '}' ], '', $tag );

	if ( $clean_tag !== 'author_first_initial' ) {
		return $tag;
	}

	return dtl_get_author_first_initial( $post );
}

add_filter( 'bricks/dynamic_data/render_content', 'dtl_render_author_first_initial_in_content', 20, 3 );
add_filter( 'bricks/frontend/render_data', 'dtl_render_author_first_initial_in_content', 20, 2 );

function dtl_render_author_first_initial_in_content( $content, $post, $context = 'text' ) {
	if ( strpos( $content, '{author_first_initial}' ) === false ) {
		return $content;
	}

	$value = dtl_get_author_first_initial( $post );

	return str_replace( '{author_first_initial}', $value, $content );
}

function dtl_get_author_first_initial( $post ) {
	$author_id = get_post_field( 'post_author', $post->ID );

	if ( ! $author_id ) {
		return '';
	}

	$display_name = get_the_author_meta( 'display_name', $author_id );

	if ( empty( $display_name ) ) {
		return '';
	}

	return strtoupper( substr( $display_name, 0, 1 ) );
}
