package com.jsl26tp.jsl26tp.inquiry.service;

import com.jsl26tp.jsl26tp.common.BusinessException;
import com.jsl26tp.jsl26tp.common.ErrorCode;
import com.jsl26tp.jsl26tp.inquiry.domain.Inquiry;
import com.jsl26tp.jsl26tp.inquiry.mapper.InquiryMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

/**
 * お問い合わせ Service (ユーザー向け)
 *
 * 유저가 문의를 등록/조회/삭제하는 비즈니스 로직 담당
 * - 관리자 문의 처리(답변 등)는 AdminService에서 담당
 * - 예외는 BusinessException → GlobalExceptionHandler가 ApiResponse.error()로 변환
 */
@Service
@RequiredArgsConstructor
public class InquiryService {

    private final InquiryMapper inquiryMapper;

    // 내 문의 내역 조회 (Mapper 메서드명이 findByWriterId인 것 확인!)
    public List<Inquiry> findByWriterId(Long userId) {
        return inquiryMapper.findByWriterId(userId);
    }

    /**
     * 문의 등록
     *
     * 검증:
     * 1. title이 비어있지 않은지 확인
     * 2. content가 비어있지 않은지 확인
     *
     * @param inquiry writerId, title, content 필수
     * @throws BusinessException BAD_REQUEST — title/content가 비어있을 때
     */
    @Transactional
    public void createInquiry(Inquiry inquiry) {

        // title 빈값 체크
        if (inquiry.getTitle() == null || inquiry.getTitle().trim().isEmpty()) {
            throw new BusinessException(ErrorCode.BAD_REQUEST);
        }

        // content 빈값 체크
        if (inquiry.getContent() == null || inquiry.getContent().trim().isEmpty()) {
            throw new BusinessException(ErrorCode.BAD_REQUEST);
        }

        inquiryMapper.insertInquiry(inquiry);
    }

    /**
     * 문의 상세 조회
     *
     * @throws BusinessException INQUIRY_NOT_FOUND — 문의가 존재하지 않을 때
     */
    public Inquiry getInquiryDetail(Long id) {
        Inquiry inquiry = inquiryMapper.findById(id);
        if (inquiry == null) {
            throw new BusinessException(ErrorCode.INQUIRY_NOT_FOUND);
        }
        return inquiry;
    }

    /**
     * 문의 삭제 (소프트 삭제)
     *
     * 검증: 본인이 작성한 문의만 삭제 가능
     *
     * @param id       문의 ID
     * @param writerId 요청한 유저의 ID (본인 확인용)
     * @throws BusinessException INQUIRY_NOT_FOUND — 문의가 존재하지 않을 때
     * @throws BusinessException ACCESS_DENIED — 본인 문의가 아닐 때
     */
    @Transactional
    public void deleteInquiry(Long id, Long writerId) {
        Inquiry inquiry = inquiryMapper.findById(id);

        if (inquiry == null) {
            throw new BusinessException(ErrorCode.INQUIRY_NOT_FOUND);
        }

        // 본인 확인
        if (!inquiry.getWriterId().equals(writerId)) {
            throw new BusinessException(ErrorCode.ACCESS_DENIED);
        }

        inquiryMapper.deleteInquiry(id);
    }
}