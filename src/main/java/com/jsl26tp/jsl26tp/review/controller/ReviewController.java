package com.jsl26tp.jsl26tp.review.controller;

import com.jsl26tp.jsl26tp.common.ApiResponse;
import com.jsl26tp.jsl26tp.review.domain.Review;
import com.jsl26tp.jsl26tp.review.service.ReviewService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@RestController
@RequestMapping("/api/reviews")
@RequiredArgsConstructor
public class ReviewController {

    private final ReviewService reviewService;

    @PostMapping("/write")
    public ApiResponse<String> writeReview(
            @ModelAttribute Review review,
            @RequestParam(value = "files", required = false) List<MultipartFile> files) {

        reviewService.writeReview(review, files);

        return ApiResponse.ok("OK");
    }

    @GetMapping("/{id}")
    public ApiResponse<Review> getReviewDetail(@PathVariable("id") Long id) {

        // 서비스 호출 (리뷰 정보 + 작성자 닉네임 + 이미지 리스트가 담긴 객체 반환)
        Review review = reviewService.getReviewDetail(id);

        return ApiResponse.ok(review);
    }

}
