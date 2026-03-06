package com.jsl26tp.jsl26tp.review.service;

import com.jsl26tp.jsl26tp.review.domain.Review;
import com.jsl26tp.jsl26tp.review.mapper.ReviewMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
@RequiredArgsConstructor // 누나 규칙: 생성자 주입
public class ReviewService {

    private final ReviewMapper reviewMapper;

    // 내가 쓴 리뷰 목록 조회
    public List<Review> findByUserId(Long userId) {
        return reviewMapper.findByUserId(userId);
    }
}