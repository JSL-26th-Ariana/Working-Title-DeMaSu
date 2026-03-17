package com.jsl26tp.jsl26tp.toilet.mapper;

import com.jsl26tp.jsl26tp.toilet.domain.RecentView;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import java.util.List;

@Mapper
public interface RecentViewMapper {

    // 최근 조회 기록 저장 (UPSERT: 이미 있으면 시간만 업데이트)
    void upsertView(@Param("userId") Long userId, @Param("toiletId") Long toiletId);

    // 사용자의 최근 조회 목록
    List<RecentView> findByUserId(@Param("userId") Long userId);

    // 조회 기록 삭제
    void deleteByUserId(@Param("userId") Long userId);

    // 개별 삭제 추가
    void deleteByToiletId(@Param("userId") Long userId, @Param("toiletId") Long toiletId);
}
