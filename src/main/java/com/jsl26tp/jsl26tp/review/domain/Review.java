package com.jsl26tp.jsl26tp.review.domain;

import lombok.Data;
import java.time.LocalDateTime;
import java.util.List;

@Data
public class Review {
    private Long id;
    private Long toiletId;
    private Long userId;
    private String cleanScore;
    private String tags;
    private String content;
    private String status;           // ACTIVE, HIDDEN
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private LocalDateTime deletedAt;

    // JOIN 용 추가 필드
    private String nickname;         // 작성자 닉네임
    private String iconUrl;          // 작성자 아이콘
    private List<ReviewImage> images; // 리뷰 이미지 목록
}
