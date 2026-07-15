<?php
/**
 * Bricks Dynamic Tag: {dtl_post_date_reading_time}
 * Returns post date + reading time in Malay format.
 *
 * Example output: "July 9, 2026 · 4 min baca"
 * Replaces the {echo:post_date_reading_time} tag to avoid English "min read" text.
 */

add_filter( 'bricks/dynamic_tags_list', 'dtl_register_post_date_reading_time_ms_tag' );

function dtl_register_post_date_reading_time_ms_tag( $tags ) {
	$tags[] = [
		'name'  => '{dtl_post_date_reading_time}',
		'label' => 'Post Date + Reading Time (MS)',
		'group' => 'Post',
	];
	return $tags;
}

add_filter( 'bricks/dynamic_data/render_tag', 'dtl_render_post_date_reading_time_ms', 20, 3 );

function dtl_render_post_date_reading_time_ms( $tag, $post, $context = 'text' ) {
	if ( ! is_string( $tag ) ) {
		return $tag;
	}

	$clean_tag = str_replace( [ '{', '}' ], '', $tag );

	if ( $clean_tag !== 'dtl_post_date_reading_time' ) {
		return $tag;
	}

	return dtl_get_post_date_reading_time_ms( $post );
}

add_filter( 'bricks/dynamic_data/render_content', 'dtl_render_post_date_reading_time_ms_in_content', 20, 3 );
add_filter( 'bricks/frontend/render_data', 'dtl_render_post_date_reading_time_ms_in_content', 20, 2 );

function dtl_render_post_date_reading_time_ms_in_content( $content, $post, $context = 'text' ) {
	if ( strpos( $content, '{dtl_post_date_reading_time}' ) === false ) {
		return $content;
	}

	$value = dtl_get_post_date_reading_time_ms( $post );

	return str_replace( '{dtl_post_date_reading_time}', $value, $content );
}

function dtl_get_post_date_reading_time_ms( $post ) {
	if ( ! $post || ! isset( $post->ID ) ) {
		return '';
	}

	$post_date = get_the_date( 'F j, Y', $post->ID );
	$minutes   = dtl_estimate_reading_minutes( $post );

	return sprintf( '%s · %d min baca', $post_date, $minutes );
}

function dtl_estimate_reading_minutes( $post ) {
	$content = get_post_field( 'post_content', $post->ID );

	if ( empty( $content ) ) {
		return 1;
	}

	// Strip shortcodes and HTML, then count words.
	$text  = strip_shortcodes( $content );
	$text  = wp_strip_all_tags( $text );
	$words = str_word_count( $text );

	$minutes = (int) ceil( $words / 200 );

	return max( 1, $minutes );
}
