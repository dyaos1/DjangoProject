from django.db import models

# static path
import os
from django.conf import settings
STATIC_PATH = settings.STATIC_DIR
MEDIA_PATH = settings.MEDIA_ROOT


class MetaData(models.Model):
    """
    메타데이터: 모델 hierarchy 최상의 기본 모델. 다른 모델의 forenkey 역할을 하며, 거의 모든 template context에 호출됨
    필수 입력 정보: building_name, start_date, end_date
    나머지는 initializer()로 생성
    """
    building_name = models.CharField(max_length=20)
    report_name = models.CharField(max_length=50, null=True)

    class CompanyChoices(models.TextChoices):
        ELIM="elim"
        EL= "el"

    type_third = models.BooleanField(default=False)
    company = models.CharField(
        max_length=10,
        choices=CompanyChoices.choices,
        default=CompanyChoices.ELIM
    )
    file_path = models.CharField(max_length=50, null=True)

    start_date = models.DateField()
    end_date = models.DateField()

    # 초기화시 자동생성(시작일, 종료일로 결정되는 정보들)
    year = models.CharField(max_length=8, null=True)
    month = models.CharField(max_length=8, null=True)
    day = models.CharField(max_length=8, null=True)
    semi = models.CharField(max_length=8, null=True)

    def initializer(self):
        """
        필수 정보 외의 필드들을 생성하는 메서드
        """
        self.year = str(self.startDate).split('-')[0]
        self.month = str(self.startDate).split('-')[1]
        self.day = str(self.startDate).split('-')[2]
        self.semi = "하반기" if int(self.month) > 6 else "상반기"

        reportType = "3종" if self.type_third else ""
        reportName = str(self.building_name) + " " + str(self.year) + "년 " + str(self.semi) + " " + reportType
        self.report_name = reportName

        self.file_path = os.path.join(STATIC_PATH, str(self.id) + " " + self.building_name)

        self.save()

    def __str__(self):
        return self.building_name


class PrintHistory(models.Model):
    print_history = models.ForeignKey(MetaData, on_delete=models.CASCADE)

    # 0. 표지
    cover = models.BooleanField(default=False)
    partialPhoto = models.BooleanField(default=False)
    certification_and_engineers = models.BooleanField(default=False)
    resultTable = models.BooleanField(default=False)

    # 1. 서론
    intro = models.BooleanField(default=False)

    # 2. 일반사항, 
    inspection_status = models.BooleanField(default=False)
    management_status = models.BooleanField(default=False)
    # bd_maintenanceHistory = models.BooleanField(default=False)
    # be_previousResult = models.BooleanField(default=False)

    # 3. 결함조사
    research_method = models.BooleanField(default=False)
    defectStatus = models.BooleanField(default=False)
    publicPart = models.BooleanField(default=False)
    locationMap = models.BooleanField(default=False)
    
    # 4. 종합결론
    conclusion = models.BooleanField(default=False)
    
    # 5. 보수방안
    repair_method = models.BooleanField(default=False)

    # 6. 부록 : 과업지시서, 건축물대장, 시설물대장, 사진첩, 기타
    workOrder = models.BooleanField(default=False)
    BML = models.BooleanField(default=False)
    FML = models.BooleanField(default=False)
    photo_album = models.BooleanField(default=False)
    etc = models.BooleanField(default=False)

    # 합침 기록
    merger = models.BooleanField(default=False)


class ContractInfo(models.Model):
    contract = models.OneToOneField(MetaData, on_delete=models.CASCADE)

    # 건축물명 + 년도 + 반기 + 정기안전점검
    contract_name = models.CharField(max_length=64)
    contract_agency = models.CharField(max_length=64)
    contract_joint = models.CharField(max_length=16, default="독자수행100%")
    contract_method = models.CharField(max_length=32, default="수의계약")
    contract_money = models.CharField(max_length=16)
    
    def __str__(self):
        return self.contract_name